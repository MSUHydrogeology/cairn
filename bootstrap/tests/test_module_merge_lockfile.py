"""The module-merge ⇄ install-lockfile divergence defect (lockfile loss).

`run_module_merge_pass` merges module content into slots in *tracked* target
files (`AGENTS.md` is the shipped case) AFTER `install_core` and BEFORE
`write_install_lockfile`. That writer recomputes, per tracked file, an
expected-clean-install byte string `would` and refuses to write ANY lockfile
or base-template cache if any file differs. So a merge that actually lands
made the install finish with **no integrity baseline and no upgrade
ancestor** — silently, at exit 0.

The fix follows the `dev/PLANNING.md` onboarding-overlay precedent
(`_rendered_onboarding_overlay`, whose docstring states the rule): the live
merge and the writer's `would` computation derive both *which merges apply*
(`module_merge_directives`) and *what a merge does to the bytes*
(`resolve_slot_merge`, via `apply_module_merges`) from ONE shared function
each, so they cannot drift. The divergence guard is NOT weakened: `would`
now carries the *expected* post-merge bytes, so only those bytes match.

What is pinned here:

* **Acceptance (live install)** — a real `main()` install whose module set
  fires a landing merge writes `dev/.cairn/cairn-lock.yml` and populates the
  base cache. Non-vacuous: the test also asserts the merged prose is in the
  installed `AGENTS.md`, so it fails if the merge silently stopped landing.
* **Fail-closed preserved** — tampering a merge target still makes the
  writer refuse.
* **No drift by construction** — the two call sites of each shared function,
  checked structurally, plus the CLI handing both paths the same `modules`
  list (the precondition that makes the two directive *sequences* equal).
* **Order-dependence, stated not assumed** — the merged bytes are a function
  of the directive *sequence*, not just the set (first-wins on a shared
  slot); the sequence contract is module order → spec order → document
  order.
* **Non-merge files unaffected** and **verbatim specs still skipped**.

Fixture note: Cairn's shipped `templates/core/AGENTS.md` ships PROSE inside
its `security-verification` slot, so the only shipped merge directive
resolves `conflict-deferred` and never writes the target — which is why the
defect is latent in-tree rather than firing on a stock install. The live
tests therefore install from a COPY of `templates/` whose slot body is
emptied: that is the merge mechanism's designed happy path (`inserted`), and
the exact state in which the defect fires.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_module_merge_lockfile.py
"""
from __future__ import annotations

import ast
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import main  # noqa: E402
from bootstrap._scaffold import install as INS  # noqa: E402
from bootstrap._scaffold import slotmerge as SM  # noqa: E402
from bootstrap._scaffold.config import InstallSpec  # noqa: E402
from bootstrap._scaffold.lockfile import read_lockfile  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_PKG = CAIRN_ROOT / "bootstrap" / "_scaffold"

#: The one shipped module carrying `cairn:merge-target` directives, and the
#: tracked file + slot it merges into.
_MERGE_MODULE = "security-verification"
_MERGE_TARGET = "AGENTS.md"
_MERGE_SLOT = "security-verification"

#: A distinctive fragment of the merged content (from
#: templates/modules/default-on/security-verification.md's merge block), used
#: to prove the merge actually landed rather than silently no-op'ing.
_MERGED_FRAGMENT = "scripts/run_security_verification.py"

#: The module set the live-install fixture selects: the default-on set plus
#: the merge-declaring module.
_PROFILE_MODULES = (
    "lifecycle-metrics",
    "reflections",
    "claim-check",
    "fold-back-ledger",
    "incident-trackers",
    "documentation-plan",
    "content-security",
    _MERGE_MODULE,
)


def _empty_the_slot(path: Path, slot: str) -> None:
    """Blank the named slot's body in *path* so a module merge INSERTS."""
    text = path.read_text(encoding="utf-8")
    opener = f"<!-- cairn:slot {slot} -->"
    closer = f"<!-- cairn:end {slot} -->"
    o = text.index(opener) + len(opener)
    c = text.index(closer)
    path.write_text(text[:o] + "\n" + text[c:], encoding="utf-8")


@pytest.fixture(scope="module")
def merging_cairn_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A Cairn root whose `templates/` is a copy with the merge target's slot
    body emptied, so the shipped directive lands as `inserted`.

    Only `templates/` is copied; the engine under test is the real one,
    reached through `--cairn-root`.
    """
    root = tmp_path_factory.mktemp("merging-cairn-root")
    shutil.copytree(
        CAIRN_ROOT / "templates", root / "templates",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    _empty_the_slot(root / "templates" / "core" / _MERGE_TARGET, _MERGE_SLOT)
    return root


def _scaffold(target: Path, cairn_root: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: MergeLockfileTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in _PROFILE_MODULES),
        encoding="utf-8",
    )
    return main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(cairn_root), "--allow-dev", "--non-interactive",
    ])


# --- Acceptance: the live install keeps its lockfile -----------------------

def test_live_install_writes_a_lockfile_when_a_module_merge_lands(
    merging_cairn_root: Path, tmp_path: Path,
) -> None:
    """The defect's actual signature: a landing module merge must not cost
    the adopter their lockfile or base-template cache.

    A unit test on `write_install_lockfile` cannot stand in for this — the
    defect only appears when the live merge pass has already rewritten the
    target between `install_core` and the writer.
    """
    rc = _scaffold(tmp_path, merging_cairn_root)
    assert rc == 0

    # Non-vacuity: the merge must actually have LANDED. If the fixture stops
    # producing an `inserted` merge, this test would otherwise pass while
    # exercising nothing.
    agents = (tmp_path / _MERGE_TARGET).read_text(encoding="utf-8")
    assert _MERGED_FRAGMENT in agents, (
        "the module merge did not land in the installed AGENTS.md -- this "
        "test is no longer exercising the defect"
    )
    assert not list(tmp_path.glob("*.cairn-merge-pending")), (
        "the merge deferred to a side-file instead of inserting"
    )

    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    assert lock_path.is_file(), (
        "cairn-lock.yml was NOT written -- write_install_lockfile's `would` "
        "has diverged from the module-merge pass, so the adopter has no "
        "integrity baseline and no upgrade ancestor"
    )
    lock = read_lockfile(tmp_path)
    assert lock is not None
    assert lock.get("files"), "lockfile has no files[] -- looks malformed"

    # The base-template cache is the other half the refusal withheld.
    cached = list((tmp_path / "dev" / ".cairn" / "base").rglob("*"))
    assert [p for p in cached if p.is_file()], (
        "the base-template cache is empty -- the writer refused"
    )
    # The merge target itself is tracked, and its recorded hash is the
    # POST-merge hash (that is what `would` now computes).
    tracked = {rec["dst"] for rec in lock["files"]}
    assert _MERGE_TARGET in tracked


# --- Constraint 1: fail-closed is preserved -------------------------------

def test_writer_still_refuses_when_a_merge_target_is_tampered(
    merging_cairn_root: Path, tmp_path: Path,
) -> None:
    """Tampering the merge target must STILL land it in `diverged` and still
    refuse to write any lockfile or cache.

    The overlay must widen `would` to exactly the expected post-merge bytes
    — not to "anything the adopter has in that file".
    """
    assert _scaffold(tmp_path, merging_cairn_root) == 0
    lock = read_lockfile(tmp_path)
    assert lock is not None  # the fix is in place

    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    cache_dir = tmp_path / "dev" / ".cairn" / "base"
    lock_path.unlink()
    shutil.rmtree(cache_dir)

    target_file = tmp_path / _MERGE_TARGET
    target_file.write_text(
        target_file.read_text(encoding="utf-8")
        + "\n<!-- tampered after the merge -->\n",
        encoding="utf-8",
    )

    again = INS.write_install_lockfile(
        tmp_path, merging_cairn_root, merging_cairn_root / "templates",
        tokens=dict(lock["tokens"]),
        modules=list(_PROFILE_MODULES),
        optional=[],
        profile=lock["profile"],
    )
    assert again is None, (
        "the divergence guard was weakened: a tampered merge target no "
        "longer refuses the lockfile"
    )
    assert not lock_path.exists(), "a lockfile was written despite divergence"
    assert not cache_dir.exists(), "a base cache was written despite divergence"


def test_writer_accepts_the_untampered_merge_target_on_a_rewrite(
    merging_cairn_root: Path, tmp_path: Path,
) -> None:
    """The control for the tamper test: the SAME direct re-invocation, with
    the merge target left alone, succeeds. Without this, the tamper test
    could pass because the re-invocation is broken for unrelated reasons.
    """
    assert _scaffold(tmp_path, merging_cairn_root) == 0
    lock = read_lockfile(tmp_path)
    assert lock is not None

    (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
    shutil.rmtree(tmp_path / "dev" / ".cairn" / "base")

    again = INS.write_install_lockfile(
        tmp_path, merging_cairn_root, merging_cairn_root / "templates",
        tokens=dict(lock["tokens"]),
        modules=list(_PROFILE_MODULES),
        optional=[],
        profile=lock["profile"],
    )
    assert again is not None, (
        "the writer refused an untampered tree -- the overlay does not "
        "reproduce the live merge's bytes"
    )


# --- Constraint 3: one function, called by both ---------------------------

def _calls_in(pyfile: Path, func_name: str) -> set[str]:
    """The bare-name calls made inside the named top-level function."""
    tree = ast.parse(pyfile.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return {
                n.func.id for n in ast.walk(node)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            }
    raise AssertionError(f"{func_name} not found at top level of {pyfile}")


def test_resolve_slot_merge_is_the_single_merge_decision() -> None:
    """The live merge and the writer's in-memory replay must reach the
    merge decision through the SAME function -- the rule
    `_rendered_onboarding_overlay` states for the onboarding overlay.
    """
    slotmerge = _PKG / "slotmerge.py"
    for consumer in ("merge_module_into_slot", "apply_module_merges"):
        assert "resolve_slot_merge" in _calls_in(slotmerge, consumer), (
            f"{consumer} does not call resolve_slot_merge -- a second "
            "implementation of the merge decision is the exact drift the "
            "single-source rule forbids"
        )
    # And the live path must no longer re-implement the decision itself.
    live = _calls_in(slotmerge, "merge_module_into_slot")
    for reimplemented in ("_slot_is_empty", "_normalize_for_compare"):
        assert reimplemented not in live, (
            f"merge_module_into_slot still calls {reimplemented} -- the "
            "decision has been duplicated outside resolve_slot_merge"
        )


def test_module_merge_directives_is_the_single_directive_producer() -> None:
    """Both paths must derive *which* merges apply (and in what order) from
    one function, so they cannot disagree on the directive sequence."""
    install = _PKG / "install.py"
    for consumer in ("run_module_merge_pass", "write_install_lockfile"):
        assert "module_merge_directives" in _calls_in(install, consumer), (
            f"{consumer} does not call module_merge_directives"
        )
    assert "parse_module_merge_directives" not in _calls_in(
        install, "write_install_lockfile",
    ), (
        "write_install_lockfile parses directives itself -- that is a second "
        "implementation of the directive sequence"
    )


def test_cli_hands_both_paths_the_same_module_list() -> None:
    """The precondition that makes the two directive SEQUENCES equal: the CLI
    passes one and the same `modules` binding to the live merge pass and to
    the lockfile writer. Since the merged bytes are order-dependent (see
    `module_merge_directives`), a different list -- or a re-sorted copy --
    would be a real divergence, not a cosmetic one.
    """
    tree = ast.parse((_PKG / "cli.py").read_text(encoding="utf-8"))
    merge_arg: str | None = None
    writer_arg: str | None = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id == "run_module_merge_pass":
            # (templates_root, target, modules)
            assert len(node.args) >= 3, "run_module_merge_pass call shape changed"
            assert isinstance(node.args[2], ast.Name)
            merge_arg = node.args[2].id
        elif node.func.id == "write_install_lockfile":
            for kw in node.keywords:
                if kw.arg == "modules":
                    assert isinstance(kw.value, ast.Name), (
                        "write_install_lockfile is passed a derived module "
                        "list, not the same binding the merge pass got"
                    )
                    writer_arg = kw.value.id
    assert merge_arg is not None and writer_arg is not None, (
        "could not locate both call sites in cli.py"
    )
    assert merge_arg == writer_arg, (
        f"the merge pass gets {merge_arg!r} but the lockfile writer gets "
        f"{writer_arg!r} -- the two directive sequences can differ"
    )


# --- Constraint 2: order-dependence, pinned rather than assumed away ------

def test_apply_module_merges_is_first_wins_on_a_shared_slot() -> None:
    """The merged bytes are a function of the directive SEQUENCE, not just
    the set: two directives naming the same slot resolve first-wins. Pinned
    so the order contract in `module_merge_directives` is not folded away
    into an unexamined "it's deterministic anyway"."""
    text = "<!-- cairn:slot s -->\n<!-- cairn:end s -->\n"
    first = SM.apply_module_merges(text, [("s", "AAA"), ("s", "BBB")])
    second = SM.apply_module_merges(text, [("s", "BBB"), ("s", "AAA")])
    assert "AAA" in first and "BBB" not in first
    assert "BBB" in second and "AAA" not in second
    assert first != second, (
        "order stopped mattering -- if that is now true by construction the "
        "order contract can be relaxed, but it must be re-derived, not assumed"
    )


def test_apply_module_merges_changes_bytes_only_for_an_inserted_decision() -> None:
    """Every non-`inserted` status leaves the target untouched on the live
    path, so the writer's replay must leave `would` untouched too -- else a
    `conflict-deferred` or `customized` slot re-introduces the divergence."""
    empty = "A\n<!-- cairn:slot s -->\n<!-- cairn:end s -->\nB\n"
    assert SM.apply_module_merges(empty, [("s", "X")]) != empty  # inserted

    occupied = "A\n<!-- cairn:slot s -->\nprose\n<!-- cairn:end s -->\nB\n"
    custom = (
        "A\n<!-- cairn:slot s -->\n<!-- cairn:customized -->\nmine\n"
        "<!-- cairn:end s -->\nB\n"
    )
    current = "A\n<!-- cairn:slot s -->\nX\n<!-- cairn:end s -->\nB\n"
    absent = "A\nno slots here\nB\n"
    for label, text in (
        ("conflict", occupied), ("customized", custom),
        ("already-current", current), ("missing-slot", absent),
    ):
        assert SM.apply_module_merges(text, [("s", "X")]) == text, (
            f"{label}: the replay changed bytes the live merge would not have"
        )
    assert SM.apply_module_merges(empty, []) == empty  # no directives: identity


# --- Constraints 4 + 5: scope of the overlay ------------------------------

def test_default_on_module_set_declares_exactly_the_known_merge_directive(
) -> None:
    """Constraint 4 (non-merge files unaffected), at its widest: across the
    whole shipped default-on set the overlay is exactly ONE directive, so
    every *other* target's `would` is computed exactly as before the fix.

    **This node asserted an EMPTY result** until
    `security-verification-activation` Chunk B appended
    `security-verification` -- the one module that ships a directive -- to
    `_DEFAULT_ON_MODULES`.  The premise "no default-on module declares a
    directive" is now false, so the assertion is an exact-set one rather
    than an emptiness one.  The property that mattered is intact and is
    what the mutation exercises: a *second* default-on module growing a
    merge directive still reddens this node, because the overlay must never
    grow silently.
    """
    from bootstrap._scaffold.config import _DEFAULT_ON_MODULES  # noqa: PLC0415

    found = INS.module_merge_directives(
        CAIRN_ROOT / "templates", list(_DEFAULT_ON_MODULES),
    )
    assert [(t, s) for t, s, _c in found] == [(_MERGE_TARGET, _MERGE_SLOT)]
    assert _MERGE_MODULE in _DEFAULT_ON_MODULES, (
        "the one directive above comes from a DEFAULT-ON module; if "
        f"{_MERGE_MODULE!r} ever stops being default-on this node must go "
        "back to asserting an empty overlay"
    )


def test_the_shipped_merge_module_declares_its_directive() -> None:
    """The control for the test above: `module_merge_directives` does find
    the one shipped directive, so an empty result is evidence of absence
    rather than of a broken collector."""
    found = INS.module_merge_directives(
        CAIRN_ROOT / "templates", [_MERGE_MODULE],
    )
    assert [(t, s) for t, s, _c in found] == [(_MERGE_TARGET, _MERGE_SLOT)]
    assert _MERGED_FRAGMENT in found[0][2]


def test_module_merge_directives_skips_verbatim_specs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Constraint 5: the live pass skips `verbatim` specs, so the writer must
    too -- a byte-copied asset contributes no merge."""
    mods = tmp_path / "modules"
    mods.mkdir()
    directive = (
        "<!-- cairn:merge-target: T.md > slot-{n} -->\n"
        "<!-- cairn:merge-content-start -->\nbody {n}\n"
        "<!-- cairn:merge-content-end -->\n"
    )
    (mods / "sub.md").write_text(directive.format(n="sub"), encoding="utf-8")
    (mods / "verb.md").write_text(directive.format(n="verb"), encoding="utf-8")
    monkeypatch.setitem(
        INS._MODULE_MAPPINGS, "probe-mod",
        [
            InstallSpec("sub.md", "dev/modules/sub.md"),
            InstallSpec("verb.md", "scripts/verb.md", verbatim=True),
        ],
    )
    got = INS.module_merge_directives(tmp_path, ["probe-mod"])
    assert [s for _t, s, _c in got] == ["slot-sub"], (
        "a verbatim spec contributed a merge directive"
    )


def test_module_merge_directives_order_is_module_then_spec_then_document(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The sequence contract the writer relies on, pinned end to end."""
    mods = tmp_path / "modules"
    mods.mkdir()

    def _two(a: str, b: str) -> str:
        return "".join(
            f"<!-- cairn:merge-target: T.md > {n} -->\n"
            "<!-- cairn:merge-content-start -->\n"
            f"{n}\n<!-- cairn:merge-content-end -->\n"
            for n in (a, b)
        )

    (mods / "m1s1.md").write_text(_two("a", "b"), encoding="utf-8")
    (mods / "m1s2.md").write_text(_two("c", "d"), encoding="utf-8")
    (mods / "m2s1.md").write_text(_two("e", "f"), encoding="utf-8")
    monkeypatch.setitem(INS._MODULE_MAPPINGS, "mod-1", [
        InstallSpec("m1s1.md", "dev/modules/m1s1.md"),
        InstallSpec("m1s2.md", "dev/modules/m1s2.md"),
    ])
    monkeypatch.setitem(INS._MODULE_MAPPINGS, "mod-2", [
        InstallSpec("m2s1.md", "dev/modules/m2s1.md"),
    ])

    got = [s for _t, s, _c in INS.module_merge_directives(
        tmp_path, ["mod-1", "mod-2"],
    )]
    assert got == ["a", "b", "c", "d", "e", "f"]
    swapped = [s for _t, s, _c in INS.module_merge_directives(
        tmp_path, ["mod-2", "mod-1"],
    )]
    assert swapped == ["e", "f", "a", "b", "c", "d"], (
        "module order is not honoured -- the writer and the live pass can "
        "then disagree on the sequence"
    )


def test_module_merge_directives_skips_a_missing_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matches the install's own tolerance: a spec whose source is absent
    contributes nothing rather than raising in the lockfile writer."""
    monkeypatch.setitem(
        INS._MODULE_MAPPINGS, "probe-absent",
        [InstallSpec("nope.md", "dev/modules/nope.md")],
    )
    assert INS.module_merge_directives(tmp_path, ["probe-absent"]) == []
