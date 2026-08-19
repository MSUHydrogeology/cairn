"""Fork-advisory semantics -- the comparison bytes come from the caller, never
from the tree being checked (plan ``fork-advisory-semantics``).

The detector under test is ``bootstrap/_scaffold/lockfile.py``'s
``forked_facade_findings`` / ``format_forked_facade_warning`` pair plus its two
callers (``bootstrap/verify_integrity.py`` and ``cmd_upgrade``). Before this
plan its fork test was ``hash != base_hash`` -- **both operands are fields the
tree under check writes into its own lockfile**, so a target-controlled lockfile
could suppress (or manufacture) a finding. The invariant this module exists to
pin is one sentence:

    The artifact under verification must not supply the material used to
    verify it.

Layout
------

* **The fixture matrix** (:data:`MATRIX` + :func:`build_case`) builds a
  throwaway *target* tree (facade, optional engine package, lockfile record)
  **and** an independently-parameterised throwaway *trusted-templates* tree.
  The two are separate roots on purpose: nothing the target writes can reach
  the trusted side.
* **The golden oracle** (:data:`PRE_CHANGE_FINDINGS`) is a committed
  literal -- the finding set the **pre-change** detector produced over every
  matrix row, generated once by running the engine at the named commit in a
  throwaway ``git worktree`` (see :data:`PRE_CHANGE_ORACLE_COMMIT`) and pasted
  in. It is **never** computed at test time and never derived from
  ``forked_facade_findings``: an oracle computed by the code under test agrees
  with that code by construction, however wrong the code is.
* **Nodes.** Node numbering follows the plan's node table. Nodes that assert
  *post-change* behaviour carry a ``FLIPS AT`` marker naming the chunk whose
  commit turns them green; every node names the perturbation that makes it red.

Engine imports are **function-local** throughout. That is not style: the oracle
generator loads this module under the *pre-change* engine, where
``UpstreamSource`` and ``trusted_upstream`` do not exist yet, so a module-level
import of either would make the oracle ungeneratable from the commit it must
come from.

Stdlib only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import sys
from pathlib import Path
from typing import Any, NamedTuple

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
if str(CAIRN_ROOT) not in sys.path:
    sys.path.insert(0, str(CAIRN_ROOT))

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

#: The commit whose engine produced :data:`PRE_CHANGE_FINDINGS`. It predates
#: every engine edit this plan makes, so code at that commit cannot have been
#: influenced by edits that did not exist yet. Regenerating the oracle from the
#: working tree is a review finding -- the working tree is what later chunks
#: change.
PRE_CHANGE_ORACLE_COMMIT = "79df5e5"

DEFAULT_DST = "tools/intent.py"
TRUSTED_SRC = "core/tools/intent.py"
DECOY_SRC = "core/tools/decoy.py"

UPSTREAM_BODY = b'#!/usr/bin/env python3\n"""cairn facade launcher (upstream template)."""\n'
FORKED_BODY = b'#!/usr/bin/env python3\n"""cairn facade launcher (adopter fork)."""\n'


class Case(NamedTuple):
    """One built matrix row: an independently-parameterised target tree and
    trusted-templates tree, plus the lockfile the target claims."""

    name: str
    root: Path
    target: Path
    lock: dict[str, Any]
    templates_root: Path
    src_for_dst: dict[str, str]
    ref: str | None


def _sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def build_case(
    root: Path,
    name: str,
    *,
    dst: str = DEFAULT_DST,
    disk_body: bytes | None = FORKED_BODY,
    template_body: bytes | None = UPSTREAM_BODY,
    engine: str = "populated",          # populated | empty | absent
    verbatim: bool = True,
    hash_mode: str = "disk",            # disk | trusted | stale | absent
    base_mode: str = "distinct",        # distinct | equal | absent
    lock_src: str | None = "trusted",   # "trusted" | a literal | None (omit)
    source_shape: str = "regular",      # regular|absent|symlink|symlinked-parent|absolute|dotdot
    dest_shape: str = "regular",        # regular|absent|dir|symlink|symlinked-parent|absolute|dotdot
    mapped: bool = True,
    acknowledged: bool = False,
    lock_version: str | None = "9.9.9",
    upstream_ref: str | None = "9.9.9",
    decoy: bool = False,
    planted: bool = False,
) -> Case:
    """Build one matrix row under *root*.

    The escape shapes (``symlink`` / ``symlinked-parent`` / ``absolute`` /
    ``dotdot``) plant a **canary** outside the root they escape from, and the
    canary's bytes are chosen so that an *unguarded* read would make the
    detector **suppress** the finding:

    * a source-side escape canary carries the **on-disk facade** bytes, so
      reading it would compare equal and drop the note;
    * a destination-side escape canary carries the **upstream template** bytes,
      with the same consequence.

    That is what makes nodes 3 and 13 discriminating: deleting a containment
    guard causes a wrong *suppression*, not merely a lost message.
    """
    root = Path(root).resolve()
    target = root / "repo"
    templates_root = root / "upstream" / "templates"
    outside = root / "outside"
    for d in (target, templates_root, outside):
        d.mkdir(parents=True, exist_ok=True)

    # ---- source side (the trusted templates tree) ------------------------
    src_canary = disk_body if disk_body is not None else b""
    src_rel = TRUSTED_SRC
    if source_shape == "regular":
        if template_body is not None:
            _write(templates_root / src_rel, template_body)
    elif source_shape == "absent":
        pass
    elif source_shape == "symlink":
        _write(outside / "src_canary.py", src_canary)
        link = templates_root / src_rel
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(outside / "src_canary.py")
    elif source_shape == "symlinked-parent":
        src_rel = "linked/intent.py"
        _write(outside / "stree" / "intent.py", src_canary)
        (templates_root / "linked").symlink_to(
            outside / "stree", target_is_directory=True)
    elif source_shape == "absolute":
        _write(outside / "sabs" / "intent.py", src_canary)
        src_rel = (outside / "sabs" / "intent.py").as_posix()
    elif source_shape == "dotdot":
        _write(outside / "sdd" / "intent.py", src_canary)
        src_rel = "../../outside/sdd/intent.py"
    else:  # pragma: no cover - fixture programming error
        raise ValueError(f"unknown source_shape {source_shape!r}")

    # ---- destination side (the target tree under check) ------------------
    dst_canary = template_body if template_body is not None else b""
    dst_rel = dst
    if dest_shape == "regular":
        if disk_body is not None:
            _write(target / dst_rel, disk_body)
    elif dest_shape == "absent":
        pass
    elif dest_shape == "dir":
        (target / dst_rel).mkdir(parents=True, exist_ok=True)
    elif dest_shape == "symlink":
        _write(outside / "dst_canary.py", dst_canary)
        link = target / dst_rel
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(outside / "dst_canary.py")
    elif dest_shape == "symlinked-parent":
        dst_rel = "linkdir/intent.py"
        _write(outside / "dtree" / "intent.py", dst_canary)
        (target / "linkdir").symlink_to(
            outside / "dtree", target_is_directory=True)
    elif dest_shape == "absolute":
        _write(outside / "dabs" / "intent.py", dst_canary)
        dst_rel = (outside / "dabs" / "intent.py").as_posix()
    elif dest_shape == "dotdot":
        _write(outside / "ddd" / "intent.py", dst_canary)
        dst_rel = "../outside/ddd/intent.py"
    else:  # pragma: no cover - fixture programming error
        raise ValueError(f"unknown dest_shape {dest_shape!r}")

    # ---- the engine package beside the facade ----------------------------
    # Planted for **every** `dst`, including a non-``.py`` one, and that is
    # load-bearing rather than tidy. `_facade_engine_dir` derives the engine
    # directory the same way for any name (`<dir>/_<stem>`) and only the
    # ``.py`` suffix check stops it; if the fixture withheld the directory for
    # a non-``.py`` `dst`, that row's "no finding" would be decided by the
    # *fixture* -- the engine-directory gate would drop the record whether or
    # not the suffix check existed -- and node 6's non-``.py`` row would stay
    # green under the mutation it exists to catch. Measured 2026-08-04 on
    # CPython 3.13.13, over isolated copies of `bootstrap/`: against this file
    # as it stood *before* node 6's fixture guard was added, withholding the
    # directory and deleting the suffix check left all four node-6 rows
    # passing; with the directory planted, that same deletion reddens the
    # non-``.py`` row on node 6's verdict assertion. Node 6 now asserts this
    # directory itself, so withholding it reddens that node directly.
    if engine != "absent":
        p = Path(dst_rel)
        eng = target / p.with_name("_" + p.stem)
        eng.mkdir(parents=True, exist_ok=True)
        if engine == "populated":
            (eng / "__init__.py").write_bytes(b"")

    # ---- the lockfile record the target claims ---------------------------
    if hash_mode == "disk":
        h: str | None = _sha(disk_body if disk_body is not None else b"")
    elif hash_mode == "trusted":
        h = _sha(template_body if template_body is not None else b"")
    elif hash_mode == "stale":
        h = _sha(b"a stale recorded body\n")
    elif hash_mode == "absent":
        h = None
    else:  # pragma: no cover - fixture programming error
        raise ValueError(f"unknown hash_mode {hash_mode!r}")

    if base_mode == "distinct":
        base: str | None = "sha256:" + "a" * 64
    elif base_mode == "equal":
        base = h
    elif base_mode == "absent":
        base = None
    else:  # pragma: no cover - fixture programming error
        raise ValueError(f"unknown base_mode {base_mode!r}")

    rec: dict[str, Any] = {"dst": dst_rel, "verbatim": verbatim}
    if h is not None:
        rec["hash"] = h
    if base is not None:
        rec["base_hash"] = base
    if lock_src == "trusted":
        rec["src"] = src_rel
    elif lock_src is not None:
        rec["src"] = lock_src
    if acknowledged:
        rec["fork_acknowledged"] = True

    if decoy:
        # A file that legitimately lives *inside* the trusted templates tree
        # whose bytes equal the target's forked facade. The target relabels its
        # own record to point at it. Resolving the template through rec["src"]
        # would compare equal and suppress; resolving through the trusted map
        # reads the real template and retains the finding.
        _write(templates_root / DECOY_SRC,
               disk_body if disk_body is not None else b"")
        rec["src"] = DECOY_SRC
    if planted:
        # The target carries its own templates directory holding a lookalike
        # and re-points its record at it with a `..` escape.
        _write(target / "templates" / "lookalike.py",
               disk_body if disk_body is not None else b"")
        rec["src"] = "../../repo/templates/lookalike.py"

    lock: dict[str, Any] = {"schema": 1, "files": [rec]}
    if lock_version is not None:
        lock["cairn_version"] = lock_version

    src_for_dst = {"AGENTS.md": "core/AGENTS.md"}
    if mapped:
        src_for_dst[dst_rel] = src_rel

    return Case(name, root, target, lock, templates_root, src_for_dst,
                upstream_ref)


#: The matrix. Every row is built into its own throwaway root.
MATRIX: tuple[tuple[str, dict[str, Any]], ...] = (
    # --- the headline regression: today's two live false notes -------------
    ("clean-identical", dict(disk_body=UPSTREAM_BODY)),
    ("forked-differs", dict()),
    # --- source-version skew (annotation, never a new finding) -------------
    ("skew-identical", dict(disk_body=UPSTREAM_BODY, lock_version="0.1.0")),
    ("skew-differs", dict(lock_version="0.1.0")),
    # --- unsafe SOURCE shapes: comparison refused, finding retained --------
    ("src-absolute", dict(source_shape="absolute")),
    ("src-dotdot", dict(source_shape="dotdot")),
    ("src-symlink", dict(source_shape="symlink")),
    ("src-symlinked-parent", dict(source_shape="symlinked-parent")),
    # --- no trusted row / no source file: unconfirmed, retained ------------
    ("dst-unmapped", dict(mapped=False)),
    ("src-missing", dict(source_shape="absent")),
    # --- target-supplied lookalike / relabelled src ------------------------
    ("relabelled-planted", dict(planted=True)),
    ("relabelled-decoy", dict(decoy=True)),
    ("relabelled-clean", dict(disk_body=UPSTREAM_BODY, decoy=True)),
    # --- the candidate gate (both layouts) --------------------------------
    ("engine-absent", dict(engine="absent")),
    ("engine-empty", dict(engine="empty")),
    ("non-py-dst", dict(dst="tools/notes.txt")),
    ("non-verbatim", dict(verbatim=False)),
    ("base-equal", dict(base_mode="equal")),
    ("base-absent", dict(base_mode="absent")),
    ("hash-absent", dict(hash_mode="absent")),
    # --- the operand: a recorded hash must never decide the verdict --------
    ("hash-equals-trusted", dict(hash_mode="trusted")),
    ("hash-stale", dict(hash_mode="stale")),
    # --- unsafe DESTINATION shapes ----------------------------------------
    ("dst-missing", dict(dest_shape="absent")),
    ("dst-is-dir", dict(dest_shape="dir")),
    ("dst-absolute", dict(dest_shape="absolute")),
    ("dst-dotdot", dict(dest_shape="dotdot")),
    ("dst-symlink", dict(dest_shape="symlink")),
    ("dst-symlinked-parent", dict(dest_shape="symlinked-parent")),
    # --- the verify-time opt-out ------------------------------------------
    ("acknowledged-identical",
     dict(disk_body=UPSTREAM_BODY, acknowledged=True)),
    ("acknowledged-differs", dict(acknowledged=True)),
)

MATRIX_NAMES = tuple(name for name, _ in MATRIX)


def build_matrix(root: Path) -> list[Case]:
    """Build every matrix row under its own sub-root of *root*."""
    return [build_case(root / name, name, **kw) for name, kw in MATRIX]


def project(findings: list[dict[str, Any]], root: Path) -> list[dict[str, Any]]:
    """The oracle-comparable projection of a finding list.

    Only the three fields the **pre-change** detector produced survive, and any
    absolute path is rewritten to ``<ROOT>/...`` so the committed literal does
    not embed a per-run temporary directory.
    """
    root_s = str(Path(root).resolve())
    out = [
        {
            "dst": str(f["dst"]).replace(root_s, "<ROOT>"),
            "engine": str(f["engine"]).replace(root_s, "<ROOT>"),
            "acknowledged": bool(f["acknowledged"]),
        }
        for f in findings
    ]
    return sorted(out, key=lambda d: (d["dst"], d["engine"]))


# ---------------------------------------------------------------------------
# Golden oracle -- COMMITTED LITERAL, generated at PRE_CHANGE_ORACLE_COMMIT
# in a throwaway `git worktree` under the canonical interpreter (3.13.13).
# Do not regenerate from the working tree; do not compute at test time.
# ---------------------------------------------------------------------------
PRE_CHANGE_FINDINGS: dict[str, list[dict[str, Any]]] = {
    "acknowledged-differs": [
        {"acknowledged": True, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "acknowledged-identical": [
        {"acknowledged": True, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "base-absent": [],
    "base-equal": [],
    "clean-identical": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "dst-absolute": [
        {"acknowledged": False, "dst": "<ROOT>/outside/dabs/intent.py",
         "engine": "<ROOT>/outside/dabs/_intent"},
    ],
    "dst-dotdot": [
        {"acknowledged": False, "dst": "../outside/ddd/intent.py",
         "engine": "../outside/ddd/_intent"},
    ],
    "dst-is-dir": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "dst-missing": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "dst-symlink": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "dst-symlinked-parent": [
        {"acknowledged": False, "dst": "linkdir/intent.py",
         "engine": "linkdir/_intent"},
    ],
    "dst-unmapped": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "engine-absent": [],
    "engine-empty": [],
    "forked-differs": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "hash-absent": [],
    "hash-equals-trusted": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "hash-stale": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "non-py-dst": [],
    "non-verbatim": [],
    "relabelled-clean": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "relabelled-decoy": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "relabelled-planted": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "skew-differs": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "skew-identical": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "src-absolute": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "src-dotdot": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "src-missing": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "src-symlink": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
    "src-symlinked-parent": [
        {"acknowledged": False, "dst": "tools/intent.py",
         "engine": "tools/_intent"},
    ],
}


def write_lockfile(target: Path, lock: dict[str, Any]) -> None:
    """Write *lock* where ``read_lockfile`` / ``verify_integrity`` find it."""
    p = target / "dev" / ".cairn" / "cairn-lock.yml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(lock), encoding="utf-8")


def findings_for(case: Case, *, upstream: bool = True) -> list[dict[str, Any]]:
    """Run the detector over *case*, with or without a trusted upstream."""
    from bootstrap._scaffold.lockfile import (  # noqa: PLC0415
        UpstreamSource,
        forked_facade_findings,
    )

    up = (UpstreamSource(case.templates_root, case.src_for_dst, case.ref)
          if upstream else None)
    return forked_facade_findings(case.target, case.lock, upstream=up)


def one(case: Case, *, upstream: bool = True) -> dict[str, Any]:
    """The single finding *case* must produce (fails loudly on 0 or >1)."""
    got = findings_for(case, upstream=upstream)
    assert len(got) == 1, f"{case.name}: expected exactly one finding, got {got}"
    return got[0]


# ---------------------------------------------------------------------------
# A REAL installed tree, used by the nodes that exercise the two callers end to
# end against Cairn's own trusted manifest (rather than a synthetic one).
# ---------------------------------------------------------------------------

def install_forked_target(
    target: Path, *, disk_body: bytes = FORKED_BODY, **record_overrides: Any,
) -> dict[str, Any]:
    """Install Cairn into *target*, then plant a forked ``tools/intent.py``
    beside a populated ``tools/_intent/`` and record it in the lockfile.

    ``tools/intent.py`` is in ``install_manifest(modules=None)`` -- the **full
    published catalog** -- even though this install selects no modules, which is
    exactly the property ``trusted_upstream`` pins: the trusted map is not
    narrowed by anything the target says about itself.
    """
    from bootstrap.scaffold import (  # noqa: PLC0415
        _emit_lock_yaml,
        main,
        read_lockfile,
    )

    cfg = target / "profile.yml"
    cfg.write_text("project_name: FA\ntest_command: pytest\nmodules: []\n",
                   encoding="utf-8")
    assert main(["--config", str(cfg), "--target", str(target),
                 "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    lock = read_lockfile(target)
    _write(target / "tools" / "intent.py", disk_body)
    _write(target / "tools" / "_intent" / "__init__.py", b"")
    record: dict[str, Any] = {
        "dst": "tools/intent.py", "verbatim": True,
        "hash": _sha(disk_body), "base_hash": "sha256:" + "a" * 64,
        "src": "modules/team-gated/intent.py",
    }
    record.update(record_overrides)
    lock["files"] = [r for r in lock["files"] if r.get("dst") != "tools/intent.py"]
    lock["files"].append(record)
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        _emit_lock_yaml(lock), encoding="utf-8")
    return record


def relock(target: Path, **record_overrides: Any) -> None:
    """Rewrite the planted ``tools/intent.py`` record in place (no re-install)."""
    from bootstrap.scaffold import _emit_lock_yaml, read_lockfile  # noqa: PLC0415

    lock = read_lockfile(target)
    for rec in lock["files"]:
        if rec.get("dst") == "tools/intent.py":
            for key, value in record_overrides.items():
                if value is None:
                    rec.pop(key, None)
                else:
                    rec[key] = value
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        _emit_lock_yaml(lock), encoding="utf-8")


def upgrade_stderr(target: Path, capsys, *extra: str) -> tuple[int, str]:
    """Run ``cmd_upgrade`` against *target* and return ``(rc, stderr)``."""
    from bootstrap._scaffold.upgrade import cmd_upgrade  # noqa: PLC0415

    capsys.readouterr()
    rc = cmd_upgrade(["--target", str(target), "--cairn-root", str(CAIRN_ROOT),
                      *(extra or ("--plan",))])
    return rc, capsys.readouterr().err


# ===========================================================================
# Chunk B node -- the remediation string (MAINTAINER-GATED; unfenced by the
# identity-not-name Decision amendment of 2026-08-10, which routed it here as
# scope 3 rather than a standalone trivial-class commit)
# ===========================================================================

def test_node_b2_remediation_names_no_destructive_or_no_op_action(
        tmp_path) -> None:
    """``format_forked_facade_warning``'s remediation string
    carries neither branch it shipped with pre-Chunk-B: **"remove the dormant
    engine package"** raises ``RuntimeError`` in ``tools/intent.py``'s
    ``_load_engine()`` and disables work-intent coordination outright;
    **"complete the swap (adopt the thin launcher)"** is a no-op, since the
    thin launcher is what install already places -- there is no swap left to
    complete.

    Absence of the forbidden text is only half the node (a test that merely
    forbids the bad string would pass on advice that is equally useless) --
    the surviving advice is checked by *performing* it against a real
    installed, forked ``tools/intent.py``: restore the facade from the
    upstream bytes the note names, then confirm -- through
    ``forked_facade_findings`` itself, never reimplemented here -- that the
    finding clears and that the engine package the removed branch would have
    deleted is untouched and still what ``tools/intent.py``'s own loader
    would find.

    Perturbation: restore either forbidden clause in a scratch copy of
    ``format_forked_facade_warning`` -- the forbidden-text assertions fail.
    """
    from bootstrap._scaffold.install import trusted_upstream  # noqa: PLC0415
    from bootstrap._scaffold.lockfile import (  # noqa: PLC0415
        format_forked_facade_warning,
        forked_facade_findings,
    )
    from bootstrap.scaffold import read_lockfile  # noqa: PLC0415

    target = tmp_path / "t"
    target.mkdir()
    install_forked_target(target)
    upstream = trusted_upstream(CAIRN_ROOT)

    lock = read_lockfile(target)
    findings = forked_facade_findings(target, lock, upstream=upstream)
    finding = next(f for f in findings if f["dst"] == "tools/intent.py")

    for at_upgrade in (False, True):
        text = format_forked_facade_warning(finding, at_upgrade=at_upgrade)
        lowered = text.lower()
        assert "remove the dormant engine package" not in lowered, text
        assert "complete the swap" not in lowered, text
        # The situation is still stated as fact -- only the *advice* changed.
        assert "engine package" in lowered, text

    # Perform the surviving advice for real, rather than trust its prose:
    # restore the facade from the upstream bytes the note names.
    engine_dir = target / "tools" / "_intent"
    assert engine_dir.is_dir()  # the advice never touches this
    src_rel = upstream.src_for_dst["tools/intent.py"]
    upstream_bytes = (upstream.templates_root / src_rel).read_bytes()
    (target / "tools" / "intent.py").write_bytes(upstream_bytes)

    lock_after = read_lockfile(target)
    findings_after = forked_facade_findings(target, lock_after, upstream=upstream)
    assert not any(f["dst"] == "tools/intent.py" for f in findings_after), (
        "restoring the facade from upstream must clear the finding -- "
        "otherwise the surviving advice does not describe a real fix")
    # The engine package the removed destructive branch would have deleted
    # is untouched -- the tool is left working, not merely quiet.
    assert (engine_dir / "__init__.py").is_file()


# ===========================================================================
# Chunk C nodes -- the engine core
# ===========================================================================

def test_node1_identical_facade_emits_no_note_despite_hash_ne_base_hash(
        tmp_path) -> None:
    """Node 1 -- FLIPS AT Chunk C. The headline regression: a facade
    byte-identical to its trusted template emits **no** note even when
    ``hash != base_hash``. This reproduces the two false notes Cairn's own tree
    emitted before this change.

    Perturbation: revert the verdict to ``hash != base_hash`` alone.
    """
    case = build_case(tmp_path / "n1", "n1", disk_body=UPSTREAM_BODY)
    rec = case.lock["files"][0]
    assert rec["hash"] != rec["base_hash"], "the fixture must look forked"
    assert findings_for(case) == [], (
        "a facade whose bytes equal its trusted template is not a fork")
    # The pre-change detector DID report it -- that is what makes this node the
    # regression rather than a restatement of current behaviour.
    assert PRE_CHANGE_FINDINGS["clean-identical"], "oracle sanity"


def test_node2_source_version_skew_annotates_and_never_adds_a_finding(
        tmp_path) -> None:
    """Node 2 -- FLIPS AT Chunk C. Skew is an **annotation**: the line fires,
    the finding set does not grow, and a byte-identical facade is still
    suppressed.

    Perturbation: delete the skew-annotation branch.
    """
    from bootstrap._scaffold.lockfile import (  # noqa: PLC0415
        format_forked_facade_warning,
    )

    quiet = build_case(tmp_path / "n2a", "n2a", lock_version="0.1.0",
                       disk_body=UPSTREAM_BODY)
    assert findings_for(quiet) == [], "skew must not resurrect a clean facade"

    skewed = one(build_case(tmp_path / "n2b", "n2b", lock_version="0.1.0"))
    plain = one(build_case(tmp_path / "n2c", "n2c"))
    assert skewed["skew"] and "0.1.0" in skewed["skew"] and "9.9.9" in skewed["skew"]
    assert plain["skew"] is None
    # Same finding, one extra annotation -- the set did not grow. (`upstream`
    # is excluded only because it embeds the per-case temporary root.)
    ignore = {"skew", "upstream"}
    assert {k: v for k, v in skewed.items() if k not in ignore} == \
           {k: v for k, v in plain.items() if k not in ignore}
    assert "source-version skew" in format_forked_facade_warning(
        skewed, at_upgrade=False)
    assert "source-version skew" not in format_forked_facade_warning(
        plain, at_upgrade=False)


@pytest.mark.parametrize("shape", ["absolute", "dotdot", "symlink",
                                   "symlinked-parent"])
def test_node3_unsafe_source_shapes_refuse_and_retain(tmp_path, shape) -> None:
    """Node 3 -- FLIPS AT Chunk C. Four unsafe **source** shapes: the
    comparison is refused, the finding is **retained** as ``unconfirmed``, and
    no exception escapes into the verifier that hosts the advisory.

    The fixture is built so this matters: each escape target's bytes are
    identical to the on-disk facade, so **without** the guard the finding is
    wrongly *suppressed* -- the node fails on suppression, not on a lost
    message.

    Perturbation: delete the ``_assert_safe_write`` call (or replace the
    source-side ``_guarded_read`` with a bare read).
    """
    case = build_case(tmp_path / f"n3-{shape}", "n3", source_shape=shape)
    got = one(case)
    assert got["kind"] == "unconfirmed", got
    assert got["reason"], "an unconfirmed finding must say why"


@pytest.mark.parametrize("kw,why", [
    ({"mapped": False}, "absent from the trusted install manifest"),
    ({"source_shape": "absent"}, "not an existing regular file"),
])
def test_node4_no_trusted_row_or_no_source_file_stays_unconfirmed(
        tmp_path, kw, why) -> None:
    """Node 4 -- FLIPS AT Chunk C. A ``dst`` absent from the trusted map, and a
    source file that is not there, both degrade to ``unconfirmed`` and are
    retained.

    Perturbation: make an unmapped ``dst`` fall through to "no finding".
    """
    case = build_case(tmp_path / "n4", "n4", **kw)
    got = one(case)
    assert got["kind"] == "unconfirmed"
    assert why in (got["reason"] or "")


@pytest.mark.parametrize("kw", [{"planted": True}, {"decoy": True}])
def test_node5_target_supplied_lookalike_is_not_suppressed(tmp_path, kw) -> None:
    """Node 5 -- the regression proper.

    ``planted``: the target carries its own ``templates/`` directory holding a
    file byte-identical to its forked facade and re-points its lockfile ``src``
    at it with a ``..`` escape. ``decoy``: the relabelled ``src`` names a file
    that legitimately lives *inside* the trusted templates tree whose bytes
    equal the forked facade -- the discriminating one, because a perturbation
    that resolves through ``rec["src"]`` **with** the same containment checks
    would still be fooled by it.

    Perturbation: resolve the template through ``rec["src"]`` instead of the
    trusted map.
    """
    case = build_case(tmp_path / "n5", "n5", **kw)
    got = one(case)
    assert got["kind"] == "differs-from-upstream", got
    assert got["src_relabelled"] is True


@pytest.mark.parametrize("kw,expect", [
    ({}, 1),
    ({"engine": "absent"}, 0),
    ({"engine": "empty"}, 0),
    ({"dst": "tools/notes.txt"}, 0),
])
def test_node6_engine_directory_probe_decides_both_layouts(
        tmp_path, kw, expect) -> None:
    """Node 6 -- green before and after (the candidate gate is unchanged).
    Facade + populated engine dir -> a finding; facade + no engine dir, engine
    dir with no ``.py``, or a non-``.py`` ``dst`` -> none.

    **Perturbations -- two, one per half of the gate, both run.** The engine
    probe and the ``.py`` suffix check are separate conditions and a single
    mutation does not reach both:

    * *the probe*: drop the ``engine_dir.is_dir() or glob("*.py")`` test in
      ``forked_facade_findings`` -> the ``engine="absent"`` and
      ``engine="empty"`` rows expect 0 and get 1.
    * *the suffix check*: delete ``if p.suffix != ".py": return None`` from
      ``_facade_engine_dir`` -> the ``dst="tools/notes.txt"`` row expects 0 and
      gets 1, **because the fixture plants ``tools/_notes/`` for the
      non-``.py`` row too**. Withholding that directory -- as the fixture did
      before this repair -- makes the row's verdict the fixture's rather than
      the code's: the engine gate drops the record for want of a directory, so
      before the guard below existed the row stayed green with the suffix check
      deleted. Both states were measured; see ``build_case``.

    That fixture property is asserted below rather than left to the comment on
    ``build_case``: a later fixture edit that withholds the directory reddens
    this node immediately, instead of silently returning the non-``.py`` row to
    a verdict no mutation of the code can change.
    """
    case = build_case(tmp_path / "n6", "n6", **kw)
    if kw.get("engine", "populated") != "absent":
        p = Path(case.lock["files"][0]["dst"])
        assert (case.target / p.with_name("_" + p.stem)).is_dir(), (
            f"{kw}: the fixture must plant the engine directory for this row -- "
            f"without it the row's verdict is the fixture's, not the code's")
    assert len(findings_for(case)) == expect


def test_node11_recorded_hash_never_decides_the_verdict(tmp_path, capsys) -> None:
    """Node 11 -- the operand case. A record whose
    ``hash`` equals the trusted template's hash while the on-disk bytes differ
    still produces a finding -- at **both** callers. This is the proposal
    Response's Reproduction B, re-run against real code.

    Perturbation: suppress on ``rec["hash"] == sha256(trusted)``.
    """
    from bootstrap import verify_integrity  # noqa: PLC0415

    # (a) the detector directly, over the fixture matrix row.
    case = build_case(tmp_path / "n11", "n11", hash_mode="trusted")
    assert case.lock["files"][0]["hash"] == _sha(UPSTREAM_BODY)
    assert one(case)["kind"] == "differs-from-upstream"

    # (b) caller 1 -- verify_integrity, end to end, on a real installed tree.
    target = tmp_path / "vi"
    target.mkdir()
    template = (CAIRN_ROOT / "templates" / "modules" / "team-gated"
                / "intent.py").read_bytes()
    install_forked_target(target, hash=_sha(template))
    capsys.readouterr()
    verify_integrity.verify(target)
    assert "is forked from upstream" in capsys.readouterr().err

    # (c) caller 2 -- cmd_upgrade, same record.
    _rc, err = upgrade_stderr(target, capsys)
    assert "is forked from upstream" in err


@pytest.mark.parametrize("kw", [{"dest_shape": "absent"},
                                {"dest_shape": "dir"}])
def test_node12_unreadable_destination_stays_unconfirmed(tmp_path, kw) -> None:
    """Node 12 -- FLIPS AT Chunk C. A target-side file that is missing (or is
    not a regular file) while the record claims a fork: ``unconfirmed``,
    retained, and no exception.

    Perturbation: let the missing file raise, or suppress.
    """
    case = build_case(tmp_path / "n12", "n12", **kw)
    got = one(case)
    assert got["kind"] == "unconfirmed"
    assert "not an existing regular file" in (got["reason"] or "")


@pytest.mark.parametrize("shape,refusal", [
    ("absolute", "not a repo-relative POSIX path"),
    ("dotdot", "not a repo-relative POSIX path"),
    ("symlink", "symlinked destination"),
    ("symlinked-parent", "symlinked parent"),
])
def test_node13_unsafe_destination_shapes_refuse_and_retain(
        tmp_path, monkeypatch, shape, refusal) -> None:
    """Node 13 -- FLIPS AT Chunk C. Four unsafe **destination** shapes: the
    destination-side read is **refused before a byte is read**, so no bytes from
    outside the two roots reach the comparison, and the finding is **retained**
    as ``unconfirmed``.

    Same fixture discipline as node 3 -- the canary planted outside ``target``
    is written byte-identical to the **trusted template**, so a read that
    followed the escape would compare equal and *suppress* the finding. Three
    things are asserted, not implied: retention (``one()`` demands exactly one
    surviving finding), refusal (the reason names *which* of the guard's checks
    fired, so the escape was stopped by the guard and not by luck), and
    containment (every byte read during the call came from inside ``target`` or
    the trusted templates root, and in particular the canary was never opened).

    The containment assertion is sound because the instrument is complete:
    ``Path.read_bytes`` is the **only** byte-reading call anywhere in
    ``forked_facade_findings`` or its nested ``_guarded_read`` -- checked
    against the function's own AST, not assumed -- so a read this recorder does
    not see is a read the function does not make.

    **Explicitly NOT claimed: that nothing outside ``target`` is touched.** The
    call reaches outside ``target`` on every one of the four shapes, by two
    measured channels, neither of which is a byte read:

    * the *candidate gate* runs ahead of every guard and joins
      ``target_root / engine_rel`` unchecked, so for ``absolute``, ``dotdot``
      and ``symlinked-parent`` it stats and globs an engine directory outside
      the target -- candidate **selection** is a residual, out of this
      plan's scope and recorded at the gate in ``lockfile.py``;
    * the guard itself must ``lstat`` what it is about to refuse, so for
      ``symlink`` and ``symlinked-parent`` it ``is_symlink``-stats the escape
      target before returning its refusal.

    What the guard bounds is the **comparison**: no bytes from outside the two
    roots can decide the verdict. That is the claim these assertions carry, and
    it is the claim the code supports.

    Perturbations -- **two, one per half**, both against the hazard rather than
    this node's own body, and both run:

    * *retention/refusal*: replace the destination-side ``_guarded_read`` call
      with a bare ``(target_root / dst_rel).read_bytes()``. The canary is read,
      the comparison comes out equal, the finding is suppressed, and ``one()``
      goes red on all four shapes.
    * *containment*: leave the guarded read in place and add an **unguarded**
      ``(target_root / dst_rel).read_bytes()`` ahead of it, so the escape
      happens while the verdict is unchanged. Retention, ``kind`` and
      ``reason`` all still pass; the two containment assertions below are the
      only thing that goes red. Without this second perturbation the
      containment half would be untested by the first.
    """
    case = build_case(tmp_path / f"n13-{shape}", "n13", dest_shape=shape)

    # The escape canary: the one file outside `target` carrying the *trusted
    # template's* bytes. Located before the recorder is installed, so this
    # lookup does not pollute the read log.
    canaries = [p for p in sorted((case.root / "outside").rglob("*.py"))
                if not p.is_symlink() and p.read_bytes() == UPSTREAM_BODY]
    assert len(canaries) == 1, (
        f"{shape}: the fixture must plant exactly one escape canary carrying "
        f"the trusted template's bytes; found {canaries}")
    canary = canaries[0].resolve()

    reads: list[Path] = []
    real_read_bytes = Path.read_bytes

    def _recording_read_bytes(self, *args, **kwargs):
        reads.append(Path(self))
        return real_read_bytes(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_bytes", _recording_read_bytes)
    try:
        got = one(case)
    finally:
        monkeypatch.undo()

    assert got["kind"] == "unconfirmed", got
    assert refusal in (got["reason"] or ""), got

    roots = (case.target.resolve(), case.templates_root.resolve())
    resolved = {p.resolve() for p in reads}
    # Positive control on the instrument, so the two containment assertions
    # below cannot pass on an empty log. The source side is a regular file in
    # every one of these four rows, so its read always happens *before* the
    # destination guard refuses -- an empty log would mean the recorder, not
    # the code, stopped working. (Instrument-level, by design: the hazard
    # perturbations named above are what validate the claim.)
    assert (case.templates_root / TRUSTED_SRC).resolve() in resolved, (
        f"{shape}: the recorder logged no read of the trusted template "
        f"({len(reads)} read(s) seen) -- the containment assertions below "
        f"would be vacuous")
    for read_path, actual in zip(reads, (p.resolve() for p in reads)):
        assert any(actual.is_relative_to(r) for r in roots), (
            f"{shape}: a read escaped both roots: {read_path} -> {actual}")
    assert canary not in resolved, (
        f"{shape}: the escape canary was read -- its bytes equal the trusted "
        f"template, so the finding would have been suppressed: {canary}")


def test_node14_f1_finding_set_against_the_committed_oracle(tmp_path) -> None:
    """Node 14 -- **the oracle guard**. Over every matrix row:

    * with a trusted upstream, the finding set is a **subset** of the committed
      pre-change literal (the new detector never reports more);
    * with ``upstream=None`` it is **exactly** the pre-change literal (every
      degradation path retains).

    The oracle is external to the function under test -- generated at
    :data:`PRE_CHANGE_ORACLE_COMMIT` and pasted in.

    Perturbation: widen the shared candidate gate (e.g. admit records with no
    ``base_hash``). The branch-to-branch consistency node below stays green;
    this one goes red. That asymmetry is the whole reason the oracle is
    external.
    """
    assert set(PRE_CHANGE_FINDINGS) == set(MATRIX_NAMES), (
        "the oracle and the matrix have drifted apart")
    for case in build_matrix(tmp_path):
        oracle = PRE_CHANGE_FINDINGS[case.name]
        degraded = project(findings_for(case, upstream=False), case.root)
        assert degraded == oracle, (
            f"{case.name}: upstream=None must retain the pre-change set")
        trusted = project(findings_for(case), case.root)
        assert all(f in oracle for f in trusted), (
            f"{case.name}: F1 violated -- {trusted} is not a subset of {oracle}")


def test_branch_to_branch_consistency_is_not_the_f1_guard(tmp_path) -> None:
    """A consistency aid, **explicitly not** the oracle guard: the trusted branch's
    findings are a subset of the ``upstream=None`` branch's, so the two branches
    cannot disagree about *which records are candidates*.

    It compares the code against itself, so it survives a widened candidate
    gate -- which is precisely why node 14 above uses a committed literal
    instead.
    """
    for case in build_matrix(tmp_path):
        degraded = project(findings_for(case, upstream=False), case.root)
        trusted = project(findings_for(case), case.root)
        assert all(f in degraded for f in trusted), case.name


def test_node15_r9_relabelled_src_with_clean_bytes_emits_no_note(
        tmp_path) -> None:
    """Node 15 -- a relabelled ``src`` whose disk
    bytes match the trusted upstream produces **no note at all**: the
    annotation's reach is exactly the complement of the change's success.

    Perturbation: promote ``src_relabelled`` to a standalone finding kind -- a
    note appears and this node fails.
    """
    case = build_case(tmp_path / "n15", "n15", disk_body=UPSTREAM_BODY,
                      decoy=True)
    assert case.lock["files"][0]["src"] == DECOY_SRC, "the fixture must relabel"
    assert findings_for(case) == []


def test_node18_widened_layering_assertion_still_discriminates(
        tmp_path, monkeypatch) -> None:
    """Node 18 -- *Correction 1*'s discrimination test. The widened layering
    assertion in ``test_lockfile_module.py`` still refuses anything but the
    stdlib, ``config`` and ``security``.

    **Two perturbations, both required.** (a) ``from .install import ...`` fails
    under *both* candidate widenings, so it alone cannot show the gate was not
    over-widened. (b) ``from .insecurity import ...`` **passes** under the loose
    suffix form (``"insecurity".endswith("security")`` is ``True``) and fails
    under the membership form -- (b) is what proves the widening admitted
    ``security`` rather than every leaf whose name ends in it.

    The committed assertion itself is executed (not a copy of it): the real test
    function is loaded from its file and pointed at a scratch source through the
    module ``__file__`` it reads.
    """
    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415

    probe_path = Path(__file__).with_name("test_lockfile_module.py")
    spec = importlib.util.spec_from_file_location("_tlm_probe", probe_path)
    tlm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tlm)
    check = tlm.test_lockfile_depends_only_on_stdlib_and_the_config_leaf

    real = Path(LK.__file__)
    source = real.read_text(encoding="utf-8")

    # Control: the real module passes, and so does an added `security` import.
    check()
    for allowed in ("from .config import PresetError\n",
                    "from .security import _assert_safe_write\n"):
        scratch = tmp_path / "ok.py"
        scratch.write_text(source + "\n" + allowed, encoding="utf-8")
        monkeypatch.setattr(LK, "__file__", str(scratch))
        check()
        monkeypatch.setattr(LK, "__file__", str(real))

    for refused in ("from .install import install_manifest\n",
                    "from .insecurity import _assert_safe_write\n",
                    "import bootstrap._scaffold.upgrade\n"):
        scratch = tmp_path / "bad.py"
        scratch.write_text(source + "\n" + refused, encoding="utf-8")
        monkeypatch.setattr(LK, "__file__", str(scratch))
        with pytest.raises(AssertionError):
            check()
        monkeypatch.setattr(LK, "__file__", str(real))


def test_the_three_note_shapes_render_distinctly(tmp_path) -> None:
    """The note kind is a **field on the finding**, not a reader's guess,
    and ``format_forked_facade_warning`` renders all three shapes: the
    confirmed ``differs-from-upstream`` note (naming the upstream it compared
    against), the ``unconfirmed`` note (saying the difference is from the
    install-time baseline), and the skew annotation line.

    Perturbation: drop the ``kind`` branch in the formatter -- the two notes
    become indistinguishable and this node fails.
    """
    from bootstrap._scaffold.lockfile import (  # noqa: PLC0415
        format_forked_facade_warning,
    )

    differs = one(build_case(tmp_path / "r1", "r1"))
    unconfirmed = one(build_case(tmp_path / "r2", "r2", mapped=False))
    skewed = one(build_case(tmp_path / "r3", "r3", lock_version="0.1.0"))

    a = format_forked_facade_warning(differs, at_upgrade=False)
    b = format_forked_facade_warning(unconfirmed, at_upgrade=False)
    c = format_forked_facade_warning(skewed, at_upgrade=False)
    assert "is forked from upstream" in a and "Compared against" in a
    assert "UNCONFIRMED" in b and "install-time baseline" in b
    assert "UNCONFIRMED" not in a
    assert "source-version skew" in c and "source-version skew" not in a
    # A bare pre-change-shaped finding still renders, as unconfirmed.
    bare = format_forked_facade_warning(
        {"dst": "tools/intent.py", "engine": "tools/_intent",
         "acknowledged": False}, at_upgrade=True)
    assert "upgrade:" in bare and "fork_acknowledged" not in bare


# ===========================================================================
# Chunk D nodes -- trusted_upstream and the two callers
# ===========================================================================

def test_node9_f4_a_caller_cannot_omit_the_comparison_source(tmp_path) -> None:
    """Node 9 -- a positional two-argument call is a
    ``TypeError``: a caller that cannot say where its comparison bytes come
    from must not get a silent answer. ``upstream`` is keyword-only *and*
    has no default, so neither omitting it nor passing it positionally works.

    Perturbation: give ``upstream`` a default value.
    """
    from bootstrap._scaffold.lockfile import (  # noqa: PLC0415
        forked_facade_findings,
    )

    case = build_case(tmp_path / "n9", "n9")
    with pytest.raises(TypeError):
        forked_facade_findings(case.target, case.lock)
    with pytest.raises(TypeError):
        forked_facade_findings(case.target, case.lock, None)
    # The explicit "no trusted upstream" is legal and retains the finding.
    assert len(forked_facade_findings(
        case.target, case.lock, upstream=None)) == 1


def test_node10_the_two_callers_differ_on_the_opt_out_and_on_to_ref(
        tmp_path, capsys) -> None:
    """Node 10 -- FLIPS AT Chunk D. ``verify_integrity`` honours
    ``fork_acknowledged``; ``cmd_upgrade`` does **not** (upgrade is the active
    decision point, so the tree gets no suppression lever there); and
    ``--to <ref>`` yields ``unconfirmed`` because the templates for
    that ref are not on disk.

    Perturbation: make ``cmd_upgrade`` honour ``fork_acknowledged``.
    """
    from bootstrap import verify_integrity  # noqa: PLC0415
    from bootstrap._scaffold.upgrade import cmd_upgrade  # noqa: PLC0415

    target = tmp_path / "t"
    target.mkdir()
    install_forked_target(target, fork_acknowledged=True)

    capsys.readouterr()
    verify_integrity.verify(target)
    assert "forked from upstream" not in capsys.readouterr().err

    _rc, err = upgrade_stderr(target, capsys)
    assert "is forked from upstream" in err, (
        "upgrade must not honour the target's own opt-out")

    # --to <ref>: no trusted root for that ref -> unconfirmed, still reported.
    fake_root = tmp_path / "not-a-git-checkout"
    (fake_root / "templates").mkdir(parents=True)
    capsys.readouterr()
    rc = cmd_upgrade(["--target", str(target), "--cairn-root", str(fake_root),
                      "--to", "v0.0.1", "--plan"])
    err = capsys.readouterr().err
    assert rc == 1  # --to needs a git checkout; the advisory ran first
    assert "UNCONFIRMED" in err and "no trusted upstream" in err


@pytest.mark.parametrize("overrides", [
    {"hash": None},                                   # hash removed
    {"hash": "sha256:" + "b" * 64},                   # hash rewritten
    {"base_hash": "sha256:" + "c" * 64},              # base_hash rewritten
    {"src": "modules/default-on/lifecycle_metrics.py"},   # src relabelled
    {"src": "../../../../etc/hostname"},              # src escaping
    {"fork_acknowledged": True},                      # the opt-out
])
def test_node16_f5_parametric_no_lockfile_field_can_suppress_at_upgrade(
        tmp_path, capsys, overrides) -> None:
    """Node 16 -- the parametric operand case. On a record whose disk
    bytes differ from trusted upstream, mutating ``hash``, ``base_hash``,
    ``src`` or ``fork_acknowledged`` in turn leaves the finding standing at the
    ``cmd_upgrade`` caller.

    (Removing ``hash`` drops the record from the *candidate* gate, which is
    a residual, out of scope and stated as such -- so that row asserts the honest
    outcome rather than pretending otherwise.)

    Perturbation: key suppression on any one of the four -> that parameter
    fails.
    """
    target = tmp_path / "t"
    target.mkdir()
    install_forked_target(target)
    relock(target, **overrides)

    _rc, err = upgrade_stderr(target, capsys)
    if overrides == {"hash": None}:
        # Recorded rather than papered over: candidate selection is still
        # lock-derived, so a record with no `hash` is not examined at all.
        assert "tools/_intent" not in err
    else:
        assert "tools/_intent" in err, (
            f"{overrides} suppressed a finding it must not reach")


def test_node17_a1_trusted_upstream_takes_only_a_cairn_root(tmp_path) -> None:
    """Node 17 -- the trusted-map property, structurally.
    ``trusted_upstream`` takes exactly one parameter (``cairn_root``) and its
    ``src_for_dst`` is the destination -> source map of
    ``install_manifest(modules=None)`` -- the full published catalog, not a
    subset chosen by anything the target says.

    Perturbation: add a ``modules`` parameter, or narrow the map -> this node
    fails. It is the closest thing to a *construction* for that rule; the rule itself
    remains a written rule enforced by this node and by review, and this plan
    does not claim otherwise.
    """
    from bootstrap._scaffold.install import (  # noqa: PLC0415
        install_manifest,
        trusted_upstream,
    )

    sig = inspect.signature(trusted_upstream)
    assert list(sig.parameters) == ["cairn_root"], sig
    assert all(p.default is inspect.Parameter.empty
               for p in sig.parameters.values())

    up = trusted_upstream(CAIRN_ROOT)
    full = {dst: src for src, dst, _v in install_manifest(None)}
    assert up.src_for_dst == full
    assert up.templates_root == CAIRN_ROOT / "templates"
    # The catalog is not narrowed to what a given install selected: a
    # team-gated destination is present even though no module is installed.
    assert "tools/intent.py" in up.src_for_dst
    assert len(up.src_for_dst) > len(
        {dst for src, dst, _v in install_manifest([])})


# ===========================================================================
# Node 8 -- the advisory never changes an exit code.  Green before and
# after the change; it is also the mechanical trigger: the moment someone
# makes the advisory blocking, this node fails and the target-controlled
# fork_acknowledged opt-out must be re-decided in the same change.
# Perturbation: append a string to `violations` in verify_integrity's advisory
# loop -> this node fails.
# ===========================================================================

def test_node8_advisory_never_changes_the_exit_code(tmp_path, capsys) -> None:
    from bootstrap import verify_integrity  # noqa: PLC0415

    case = build_case(tmp_path / "n8", "n8")
    write_lockfile(case.target, case.lock)

    rc = verify_integrity.verify(case.target)
    err = capsys.readouterr().err
    # A finding really is live -- otherwise the exit-code pin is vacuous.
    assert "tools/_intent" in err, err
    assert rc == 0, f"the advisory must never change the exit code; stderr:\n{err}"
