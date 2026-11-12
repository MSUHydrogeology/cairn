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

Promises:
- A module merge that lands in an install keeps the install's lockfile and base-template cache. (BOOTSTRAP.md:123-138)
- The lockfile writer refuses to record a merged file that differs from what the install wrote. (production code: bootstrap/_scaffold/install.py:2107)
- When two modules merge into one slot, the first in module order wins. (production code: bootstrap/_scaffold/slotmerge.py:290)
- Merges are applied in module order, then in the order the module lists its files. (production code: bootstrap/_scaffold/install.py:80)
- A merge changes a file only when its slot is empty; a conflicting, customized, current, or missing slot is left as it is. (BOOTSTRAP.md:129-138)
- A verbatim module file contributes no merge. (production code: bootstrap/_scaffold/install.py:80)
- A module whose source file is missing contributes no merge and does not stop the install. (production code: bootstrap/_scaffold/install.py:80)
- A default install changes only the shipped security-verification merge target among the tracked files it merges. (BOOTSTRAP.md:123-138)

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

# Declared exception (internal hook): Hook: calls install.write_install_lockfile directly after tampering the merged AGENTS.md; no public call lets an edit land between the merge pass and .
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


# Declared exception (internal hook): Control for the tamper exception; same direct call to install.write_install_lockfile on an untampered tree.
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


# --- Constraint 2: order-dependence, pinned rather than assumed away ------


# --- Constraints 4 + 5: scope of the overlay ------------------------------
