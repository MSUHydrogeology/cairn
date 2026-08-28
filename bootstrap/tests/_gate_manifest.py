#!/usr/bin/env python3
"""Gate-integrity manifest — six-proposal superplan pre-run gate-control prerequisite.

"Tests green" is not an independent gate when the same unattended actor that the
gate governs may weaken, delete, skip, xfail, re-baseline, or allow-list the very
test that failed. This tool freezes a **pre-run manifest** of
what the gate surface *is*, so any later tampering is mechanically detectable.

Two file classes
----------------

* **Frozen set** — every pre-existing test, harness, scanner, and fixture whose
  content defines a gate's pass/fail semantics. Discovered by glob
  (``bootstrap/tests/**/*.py`` + ``bootstrap/tests/fixtures/**`` + ``scripts/*.py``)
  and byte-hashed. During the batch, **modifying or deleting a frozen file HOLDs
  by default**; *adding* a new test file is allowed and recorded. The unattended
  run must NOT decide that an edit to an existing gate is merely "strengthening."

* **Cascade-mutable set** — ``config.py`` and ``scaffold_ast_baseline.json``
  legitimately change as A/B/C/E add an ``InstallSpec`` to a registry mapping
  symbol. These are **excluded from frozen hashing**; their integrity is governed
  by the AST source-motion attest (one symbol delta) + the hardened
  ``_ast_attest.py update-symbol`` (one allowlisted baseline key, ``--expect-old``
  guarded). The manifest records their pre-run hashes + the pinned mapping-symbol
  digests so the end reviewer sees the before-state and the per-phase deltas — but
  the verifier does not HOLD on their change. (The differential oracle's baseline
  is now a **trusted git ref**, not a checked-in ``scaffold_frozen.py`` — the
  frozen-engine fixture is retired.)

Collection identity
-------------------

The manifest pins the **set of pytest node-IDs** plus the **identities of any
skip/xfail-marked nodes** (not merely counts — Codex R2-2). A dropped node
(reduced collection) or a node that *gains* a skip/xfail marker HOLDs; added
nodes are allowed and recorded.

External anchor
---------------

The manifest lives at ``bootstrap/tests/fixtures/gate_manifest.json``, committed
in the supervised pre-run prerequisite commit. ``verify --anchor-ref <SHA>``
reads the expected manifest from that **immutable git object**
(``git show <SHA>:<manifest>``) and HOLDs if the working-tree manifest differs —
so the unattended actor cannot change both the artifact and its anchor. Run the
verifier from a trusted checkout (the main ``master`` clone, not the batch
worktree) so a tampered worktree copy of *this tool* cannot whitewash itself.

Usage
-----

    python bootstrap/tests/_gate_manifest.py produce > bootstrap/tests/fixtures/gate_manifest.json
    python bootstrap/tests/_gate_manifest.py verify --anchor-ref <PREREQ_SHA>

All gate work runs under the canonical interpreter (lhm / Python 3.13); the
verifier HOLDs if the running interpreter's *minor* differs from the pinned one
(``ast.dump`` / oracle digests are interpreter-minor sensitive). Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "cairn-gate-manifest/v2"
#: v1 is still READ: the committed fixture is v1 until the single
#: re-anchor ceremony regenerates it.  `verify` accepts both; `produce`
#: only ever emits v2.  Refusing v1 before the ceremony that replaces it
#: would brick the gate it is meant to protect.
SCHEMA_V1 = "cairn-gate-manifest/v1"
_REPO = Path(__file__).resolve().parents[2]
_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
_TESTDIR_REL = "bootstrap/tests"

# Legitimately mutated by the cascade — EXCLUDED from frozen hashing; integrity
# governed by the named mechanism, not a byte hash.
CASCADE_MUTABLE: dict[str, str] = {
    "bootstrap/_scaffold/config.py":
        "AST source-motion attest — one predeclared mapping-symbol delta only (A/B/C/E)",
    "bootstrap/tests/fixtures/scaffold_ast_baseline.json":
        "_ast_attest.py update-symbol — one allowlisted baseline key, --expect-old guarded",
}

# Module-template files a refactor phase legitimately rewrites (facade splits) — plus the
# per-phase test fixtures those splits require — EXCLUDED from frozen hashing, governed by
# each phase's AST source-motion attestation + collection-identity (node-IDs / skip-xfail)
# + green suite + External-stance review, NOT a byte hash. Reported as notes by the verifier.
# Every OTHER templates/modules/**/*.py (the shipped scanner / security-gate implementations:
# content_scan*, run_security_audit, link_check, …) and every OTHER bootstrap/tests/**/*.py
# IS frozen — the batch does not edit them, and weakening a deployed scanner or a gate test
# must HOLD (Codex confirmation R2-2 Finding 2).
#
# Re-anchor 2026-06-08 (g-series, supervised + Maintainer-authorized, option-(a)): added
# test_intents_tool.py. The intent-split facade loads its `_intent/` package as a runtime
# sibling; ~50 of this file's tests exercise git-hook install by copying ONLY the facade into
# a throwaway repo (`_git_repo`, + two inline copies) and running it as a subprocess, so they
# must also stage `_intent/` beside the copied facade. That edits this gate file → the
# pre-run manifest froze it → a hard-stop the run cannot self-certify. The edit is a
# non-weakening FIXTURE change (no assertion touched); collection identity + the green suite
# + the External-stance review remain the behavioural gate. Scope is A-specific (B/C load
# their helpers in-process from the in-tree location; no fixture edit).
PHASE_SPLIT_TARGETS: dict[str, str] = {
    "templates/modules/team-gated/intent.py":
        "phase A intent-split facade — per-phase AST source-motion attestation + External-stance review",
    "templates/modules/default-on/onboarding_activate.py":
        "phase B onboarding-split facade — per-phase AST attestation + External-stance review",
    "bootstrap/tests/test_intents_tool.py":
        "phase A intent-split TEST FIXTURE — _git_repo (+ inline copies) stage the _intent/ "
        "package beside the copied facade so the git-hook subprocess tests find the engine; "
        "ASSERTIONS UNCHANGED. Governed by collection identity (node-IDs / skip-xfail) + green "
        "suite + External-stance review, not a byte hash. Supervised re-anchor, Maintainer-authorized.",
}

# Which phases may legitimately change each registry mapping symbol's digest.
MAPPING_SYMBOLS_PHASES: dict[str, list[str]] = {
    "_MODULE_MAPPINGS": ["A intent-split", "B onboarding-split", "C metrics fold-up"],
    "_SKILLS_MAPPINGS": ["E mechanization skill register"],
    "_CORE_MAPPINGS": ["E (heavier R6 pytest-wrapper option only)"],
}

# Canonical gate commands, recorded as data (run under `python` == lhm/3.13).
GATE_COMMANDS: list[dict] = [
    {"id": "bootstrap-suite",
     # The override token is part of the command, not a caveat beside it: this
     # list is copied out of the manifest and run by a person, and the broad-run
     # guard in `conftest.py` refuses the bare form with exit 4 before any test
     # executes.  A recorded command that cannot run is a worse defect than a
     # missing one, because it looks usable.
     "cmd": ["env", "CAIRN_FULL_SUITE=1",
             "python", "-m", "pytest", "bootstrap/tests/", "-q"],
     "expect": "all green; 0 skipped / 0 xfailed (the dev Bandit gate, AST attest, "
               "differential oracle, and loader-identity tests all run inside this suite)"},
    {"id": "ast-attest-verify",
     "cmd": ["python", "bootstrap/tests/_ast_attest.py", "verify",
             "bootstrap/tests/fixtures/scaffold_ast_baseline.json",
             "--known-new",
             "bootstrap/tests/fixtures/scaffold_ast_known_new.json",
             "bootstrap/_scaffold/*.py"],
     "expect": "exit 0 — every baselined symbol accounted for unchanged; the ONLY "
               "permitted CHANGED is the predeclared one-symbol mapping delta"},
    {"id": "check-cairn",
     "cmd": ["python", "scripts/check_cairn.py"],
     "expect": "green"},
    {"id": "quality-gate-neutrality",
     "cmd": ["python", "scripts/quality_gate.py", "--sub", "neutrality"],
     "expect": "green"},
]

_INTERPRETER_NOTE = ("ast.dump / differential-oracle digests are interpreter-minor "
                     "sensitive; every gate runs under the canonical lhm/3.13 interpreter")


# ---------------------------------------------------------------------------
# The guarded Git boundary for THIS module
# ---------------------------------------------------------------------------
#
# There is **one guarded
# launcher per executable boundary**, not one shared module: this file,
# `_gate_preflight.py`, `bootstrap/security_check.py` and
# `bootstrap/container/verify-ref.sh` are four independently executable entry
# points, and a Python launcher cannot serve the shell one.
#
# Before this, the two git calls below ran bare `["git", ...]` with the
# operator's whole environment -- so `GIT_DIR`, `GIT_CONFIG_GLOBAL`,
# `GIT_REPLACE_REF_BASE` and friends could steer the anchor reachability check
# and the manifest read that decide whether a release proceeds.

#: Config pinned on every invocation. Read-only commands, but `core.quotePath`
#: and the pager change what the caller *parses*, and `protocol.*` bounds what a
#: hostile ref could reach for.
_STERILE_CONFIG = {
    "core.quotePath": "false",
    "core.pager": "cat",
    "core.hooksPath": "/dev/null",
    "protocol.version": "2",
}


def _sterile_env() -> dict[str, str]:
    """Drop every ``GIT_*`` rather than denylisting by name.

    The steering set is large and grows between releases, so removing all of it
    and putting back only what is needed fails safe where an enumerated
    denylist does not.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git(*args: str, repo: Path,
         want_bytes: bool = False) -> subprocess.CompletedProcess:
    """The single sterile-Git launcher for this module.

    **Nothing else here may call ``subprocess`` with ``git``.** The guarantees
    hold only if there is exactly one place they are applied;
    `test_gate_manifest.py` pins that at the source level.
    """
    overrides: list[str] = []
    for key, value in _STERILE_CONFIG.items():
        overrides += ["-c", f"{key}={value}"]
    # Bind the invocation to *this* directory. `git -C <path>`
    # **discovers upward**, so without this a non-repository directory nested
    # anywhere under a checkout answers with that checkout -- and the path this
    # bites is `produce`'s own: its repository is
    # `raw_tree`'s `tempfile.mkdtemp()`, so a `TMPDIR` under a checkout would
    # make `produce` read *that* repository's object format and HEAD tree and
    # stamp its modes and oids into the candidate manifest.
    #
    # Repository binding is one of five properties required
    # per guarded boundary; this launcher had the other four.
    # `_gate_preflight._require_worktree_root` is the same idea enforced by
    # refusal; here the correct behaviour for a non-repository is to *report*
    # that (`_object_format` returns None), so the binding is a config pin
    # rather than a raise.
    # Resolve the start path before ceiling it. `GIT_CEILING_DIRECTORIES`
    # is compared against the *logical* path, so a symlink pointing at a nested
    # non-repository directory escaped the ceiling entirely and discovered the
    # target repository -- measured by the security review against the previous
    # version of this line, which set the ceiling from the unresolved parent.
    start = Path(repo).resolve()
    return subprocess.run(
        ["git", "-C", str(start), *overrides, *args],
        capture_output=True, text=not want_bytes, check=False,
        env={**_sterile_env(),
             "GIT_CEILING_DIRECTORIES": str(start.parent),
             "GIT_DISCOVERY_ACROSS_FILESYSTEM": "0",
             # The same pin applies to this boundary: it is documented
             # read-only and had the same optional-index-write behaviour.
             "GIT_OPTIONAL_LOCKS": "0"},
    )


# --- v2: Git-native identity alongside the content digest ------------------
#
# R1-C.  Each tracked entry records committed **mode**, full Git **blob oid**,
# and lowercase **SHA-256** over the exact blob bytes, with the repository's
# object format at the manifest level.
#
# Both values are kept, deliberately.  The Git oid supplies repository-native
# identity, the committed mode, and tracked/untracked state -- facts Git owns.
# SHA-256 preserves an independent content digest that does not depend on the
# repository's object format, which is what the out-of-band exact-byte review
# needs.  **Neither is authenticity**: the checkpoint signature and the pinned
# roster own that claim, and no label here may imply otherwise.

_OBJECT_FORMAT_WIDTH = {"sha1": 40, "sha256": 64}


def _object_format(repo: Path) -> "str | None":
    """The repository's object format, or ``None`` when *repo* is not one.

    **Why `None` rather than a refusal, and why that is not a fallback.**
    `produce` is invoked as a CLI from a **materialized raw tree** -- the
    evidence stage extracts the anchored checker into a directory with no
    `.git`, deliberately, so the candidate's own code cannot interfere. There
    is no repository there to ask. Refusing would break the isolation that
    makes the evidence trustworthy; guessing `sha1` would be the defect this
    whole chunk removes. Absence is reported as absence.

    The Git-native half of the manifest is then supplied by the checker's own
    `_gate_preflight.rederive_static_manifest`, which always has the real
    repository -- and that is the stronger arrangement anyway: **mode and oid
    are derived by the trusted side and never accepted from the candidate.**
    """
    r = _git("rev-parse", "--show-object-format", repo=repo)
    fmt = (r.stdout or "").strip()
    if r.returncode != 0:
        return None
    if fmt not in _OBJECT_FORMAT_WIDTH:
        raise RuntimeError(
            f"unrecognised object format {fmt!r} in {str(repo)!r}; refusing "
            f"rather than assuming sha1")
    return fmt


def _tree_blobs(repo: Path, commit: str = "HEAD") -> dict:
    """``rel -> (mode, oid)`` from the commit's raw tree.

    Mode and oid come from **Git**, not from the filesystem: a worktree stat
    cannot tell a committed 100644 from a 100755 that was chmod'd after
    checkout, and it has no oid at all.
    """
    r = _git("ls-tree", "-r", "-z", "--full-tree", commit, repo=repo)
    if r.returncode != 0:
        raise RuntimeError(
            f"could not read the tree of {commit!r}: {(r.stderr or '').strip()}")
    out = {}
    for rec in (r.stdout or "").split("\0"):
        if not rec.strip():
            continue
        meta, _, rel = rec.partition("\t")
        parts = meta.split()
        if len(parts) < 3:
            continue
        mode, _typ, oid = parts[0], parts[1], parts[2]
        out[rel] = (mode, oid)
    return out


def _blob_sha256(repo: Path, oid: str) -> str:
    """SHA-256 over the **committed blob's** bytes, read through Git.

    Not the worktree's bytes.  Mixing the two is a real defect and it was
    caught by a test: `produce` originally hashed the worktree while taking
    mode and oid from `ls-tree HEAD`, so for any dirty file the manifest
    carried two digests describing *different content*, and a target tree
    holding the worktree bytes then failed the oid comparison.

    R1-C: production obtains mode and oid from the candidate commit's raw tree
    and computes SHA-256 independently over the raw blob bytes -- independently
    of Git's hashing, over the same bytes Git hashed.
    """
    r = _git("cat-file", "blob", oid, repo=repo, want_bytes=True)
    if r.returncode != 0:
        raise RuntimeError(f"could not read blob {oid}: {r.stderr!r}")
    return hashlib.sha256(r.stdout).hexdigest()


def _entry_sha256(entry) -> str:
    """The SHA-256 from a frozen entry, in either schema.

    v1 stored a bare digest string; v2 stores a dict.  Reading both is what
    lets the gate keep working between this change and the ceremony that
    regenerates the committed fixture.
    """
    return entry if isinstance(entry, str) else entry["sha256"]


def _sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _frozen_files(repo: Path = _REPO) -> list[str]:
    """Discover the frozen gate surface by glob, minus cascade-mutable files and
    the manifest artifact itself."""
    exclude = set(CASCADE_MUTABLE) | set(PHASE_SPLIT_TARGETS) | {_MANIFEST_REL}
    found: set[str] = set()
    # ``bootstrap/*.py`` (top-level, NON-recursive) freezes the gate-defining engine
    # modules — security_check.py (the single source of the Bandit ALLOWLIST +
    # scan_targets), verify_integrity.py, check_module_body_coverage.py, and the
    # scaffold.py launcher — which the in-suite security/integrity gates import. The
    # cascade edits ``bootstrap/_scaffold/config.py`` (a subdir, not matched here),
    # so these stay frozen; a launcher change during the batch is a deliberate HOLD.
    # ``templates/modules/**/*.py`` freezes the shipped scanner / security-gate
    # implementations (content_scan*, run_security_audit, link_check, …); the three
    # phase-split facade targets are excluded above (PHASE_SPLIT_TARGETS).
    for pattern in ("bootstrap/*.py", "bootstrap/tests/**/*.py",
                    "bootstrap/tests/fixtures/**/*", "scripts/*.py",
                    "templates/modules/**/*.py"):
        for p in repo.glob(pattern):
            if not p.is_file() or "__pycache__" in p.parts:
                continue
            rel = p.relative_to(repo).as_posix()
            if rel in exclude:
                continue
            found.add(rel)
    return sorted(found)


# --- pytest plugin hook: active ONLY when CAIRN_GATE_COLLECT_OUT is set ----------
# Loaded via `-p bootstrap.tests._gate_manifest` from the _collect subprocess; a
# no-op for any normal pytest run (the module is never auto-registered as a plugin).
def pytest_collection_modifyitems(items):  # noqa: D401 (pytest hook)
    dest = os.environ.get("CAIRN_GATE_COLLECT_OUT")
    if not dest:
        return
    collected: list[str] = []
    marked: list[str] = []
    for it in items:
        collected.append(it.nodeid)
        if (it.get_closest_marker("skip") or it.get_closest_marker("skipif")
                or it.get_closest_marker("xfail")):
            marked.append(it.nodeid)
    Path(dest).write_text(json.dumps({"collected": collected, "marked": marked}),
                          encoding="utf-8")


def _collect(repo: Path = _REPO) -> tuple[list[str], list[str], int]:
    """Collect node-IDs + skip/xfail-marked identities via a clean subprocess."""
    fd, out_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        env = dict(os.environ, CAIRN_GATE_COLLECT_OUT=out_path)
        r = subprocess.run(
            [sys.executable, "-m", "pytest", _TESTDIR_REL, "--collect-only", "-q",
             "-p", "bootstrap.tests._gate_manifest", "-p", "no:cacheprovider"],
            cwd=str(repo), env=env, capture_output=True, text=True,
        )
        try:
            data = json.loads(Path(out_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return [], [], (r.returncode or 1)
        return sorted(data.get("collected", [])), sorted(data.get("marked", [])), r.returncode
    finally:
        Path(out_path).unlink(missing_ok=True)


def produce(repo: Path = _REPO) -> dict:
    """Build the gate-integrity manifest dict from the current tree."""
    collected, marked, rc = _collect(repo)
    if rc != 0:
        raise RuntimeError(
            f"pytest collection failed (rc={rc}); refusing to produce a manifest over "
            f"a non-collecting suite")
    if not collected:
        # Defence-in-depth: a real suite has hundreds of nodes. An empty set means
        # the collection plugin hook did not run (env stripped / plugin shadowed)
        # even though pytest exited 0 — refuse rather than pin a vacuous manifest.
        raise RuntimeError(
            "pytest collected zero nodes; refusing to pin a vacuous collection manifest")
    fmt = _object_format(repo)
    # Outside a repository (the raw-tree evidence path) there are no oids to
    # read, and the checker re-derives them.  Inside one, they come from Git.
    blobs = _tree_blobs(repo) if fmt is not None else {}
    frozen = {}
    untracked: list[str] = []
    for rel in _frozen_files(repo):
        if fmt is None:
            # sha256 only: the trusted re-derivation supplies mode and oid.
            frozen[rel] = _sha256(repo / rel)
            continue
        mode_oid = blobs.get(rel)
        if mode_oid is None:
            # Untracked file under a gate root.  v1 pinned its worktree bytes
            # anyway, which is the defect R1-C names: a pin that no commit
            # binds.  v2 cannot give it an oid, so it is NOT pinned -- and it
            # is recorded rather than silently dropped, because a gate file
            # nobody pinned is exactly the thing a reader needs to see.
            # `verify` HOLDs on it; refusing to *produce* would instead make
            # any work-in-progress test file unbuildable.
            untracked.append(rel)
            continue
        mode, oid = mode_oid
        if mode not in ("100644", "100755"):
            raise RuntimeError(
                f"unsupported mode {mode} for {rel}: symlinks and gitlinks are "
                f"refused (a symlink hashes through to its target)")
        frozen[rel] = {"sha256": _blob_sha256(repo, oid),
                       "mode": mode, "oid": oid}
    cascade = {
        rel: {"pre_run_sha256": _sha256(repo / rel), "governed_by": why,
              **({"mode": blobs[rel][0], "oid": blobs[rel][1]}
                 if rel in blobs else {})}
        for rel, why in sorted(CASCADE_MUTABLE.items())
        if (repo / rel).is_file()
    }
    phase_mutable = {
        rel: {"pre_run_sha256": _sha256(repo / rel), "governed_by": why,
              **({"mode": blobs[rel][0], "oid": blobs[rel][1]}
                 if rel in blobs else {})}
        for rel, why in sorted(PHASE_SPLIT_TARGETS.items())
        if (repo / rel).is_file()
    }
    baseline = json.loads((repo / "bootstrap/tests/fixtures/scaffold_ast_baseline.json")
                          .read_text(encoding="utf-8"))
    mappings = {}
    for sym, phases in MAPPING_SYMBOLS_PHASES.items():
        entry = baseline.get(f"Assign:{sym}")
        if entry is None:
            raise RuntimeError(f"mapping symbol Assign:{sym} not present in the AST baseline")
        mappings[sym] = {"baseline_digest": entry["digest"], "may_change_in_phases": phases}
    return {
        "schema": SCHEMA,
        **({"object_format": fmt} if fmt is not None else {}),
        "interpreter": {
            "version": ".".join(map(str, sys.version_info[:3])),
            "version_info": list(sys.version_info[:3]),
            "note": _INTERPRETER_NOTE,
        },
        "gate_commands": GATE_COMMANDS,
        "collection": {
            "node_count": len(collected),
            "node_ids": collected,
            "skip_xfail_marked": marked,
        },
        "frozen_files": frozen,
        "cascade_mutable": cascade,
        "phase_mutable": phase_mutable,
        "mapping_symbols": mappings,
    }


def _check_anchor(anchor_ref: str, live_text: str, *, repo: Path,
                  trusted_repo: str | Path | None,
                  trusted_ref: str) -> tuple[list[str], list[str]]:
    """The git-anchor check: the working-tree manifest must equal an IMMUTABLE
    object holding the expected manifest. Returns (holds, notes).

    Codex cross-phase finding #1: when ``trusted_repo`` is given, the expected
    manifest object is resolved from THAT repo (never the ``--target-repo``), and
    the anchor must be **reachable from a trusted ref** there — so a target that
    can edit itself cannot mint its own self-consistent replacement anchor. Without
    ``trusted_repo`` the object is read from the target and the check only proves
    the working tree matches a *target-owned* object (a loud note, not full
    external anchoring)."""
    holds: list[str] = []
    notes: list[str] = []
    if trusted_repo:
        src = Path(trusted_repo)
        reach = _git("merge-base", "--is-ancestor", anchor_ref, trusted_ref,
                     repo=src)
        if reach.returncode != 0:
            holds.append(
                f"ANCHOR: {anchor_ref} is NOT reachable from the trusted ref "
                f"'{trusted_ref}' in {src} — refusing a target-supplied anchor")
            return holds, notes
    else:
        src = repo
        notes.append(
            "ANCHOR: resolved from the TARGET repo (no --trusted-repo) — this proves "
            "the working-tree manifest matches a target-owned object, NOT an "
            "externally anchored one; pass --trusted-repo + --trusted-ref for full "
            "external anchoring")
    r = _git("show", f"{anchor_ref}:{_MANIFEST_REL}", repo=src)
    if r.returncode != 0:
        holds.append(f"ANCHOR: cannot read the manifest from {anchor_ref} in {src}: "
                     f"{r.stderr.strip() or 'git show failed'}")
    elif r.stdout != live_text:
        holds.append(f"ANCHOR: working-tree manifest differs from the immutable "
                     f"{anchor_ref} object — the manifest itself was altered")
    return holds, notes


def verify(manifest_path: str | Path, *, anchor_ref: str | None = None,
           repo: Path = _REPO, require_anchor: bool = False,
           do_collect: bool = True, out=None,
           trusted_repo: str | Path | None = None,
           trusted_ref: str = "HEAD") -> int:
    """Verify gate integrity against a manifest. 0 = intact (additions allowed),
    1 = HOLD (a gate-integrity violation).

    ``repo`` is the **target** tree being verified (the batch worktree in the
    unattended mode) — distinct from where this trusted verifier *code* runs
    (Codex confirmation R2-2 Finding 3): run the tool from the trusted ``master``
    checkout and point ``repo`` / ``--target-repo`` at the batch worktree.
    ``require_anchor=True`` makes a missing anchor a HOLD (the unattended mode).
    ``do_collect=False`` skips the pytest collection check (static-only)."""
    if out is None:
        out = sys.stderr
    manifest_path = Path(manifest_path)
    live_text = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(live_text)
    holds: list[str] = []
    notes: list[str] = []

    # 1) External git anchor — the working-tree manifest must equal an immutable,
    # externally-trusted object (resolved from --trusted-repo when given).
    if anchor_ref:
        a_holds, a_notes = _check_anchor(
            anchor_ref, live_text, repo=repo,
            trusted_repo=trusted_repo, trusted_ref=trusted_ref)
        holds.extend(a_holds)
        notes.extend(a_notes)
    elif require_anchor:
        holds.append("ANCHOR: required but no --anchor-ref supplied (unattended verification "
                     "mode demands the immutable anchor)")
    else:
        notes.append("ANCHOR: skipped (no --anchor-ref; REQUIRED for the unattended batch)")

    # 2) Interpreter minor must match (patch may differ).
    pin = manifest["interpreter"]["version_info"]
    if list(sys.version_info[:2]) != list(pin[:2]):
        holds.append(f"INTERPRETER: running {tuple(sys.version_info[:2])} != pinned "
                     f"{tuple(pin[:2])} — ast.dump/oracle digests are minor-sensitive")
    elif list(sys.version_info[:3]) != list(pin[:3]):
        notes.append(f"INTERPRETER: patch differs (running "
                     f"{'.'.join(map(str, sys.version_info[:3]))} vs pinned "
                     f"{'.'.join(map(str, pin[:3]))}); minor matches — ok")

    # 3) Frozen files — modification / removal HOLDs; new files are recorded.
    pinned_frozen = manifest["frozen_files"]
    current_frozen = {rel: _sha256(repo / rel) for rel in _frozen_files(repo)}

    # v2 adds Git-native identity.  A target whose object format differs from
    # the manifest's refuses rather than comparing incomparable ids -- an oid
    # from a sha1 repository and one from a sha256 repository are not merely
    # unequal, they are not the same kind of fact.
    pinned_fmt = manifest.get("object_format")
    live_blobs: dict = {}
    if pinned_fmt is not None:
        try:
            live_fmt = _object_format(repo)
        except RuntimeError as exc:
            holds.append(f"OBJECT-FORMAT: {exc}")
            live_fmt = None
        if live_fmt is None:
            # This branch did not exist: when the format was
            # merely *undeterminable*, neither arm fired, `live_blobs` stayed
            # empty, and every mode/oid comparison below was skipped in silence
            # -- so a mode-flipped tree that HOLDs with `.git` present reported
            # "OK — gate integrity intact" with `.git` removed. Absence was
            # treated more leniently than strangeness, which is backwards: an
            # unrecognised format already HOLDs one line up.
            #
            # `AGENTS.md`: "a tool that returns success without testing the
            # claimed property is a worse defect than no tool, because it is
            # silent." The manifest pins a format; if we cannot read the
            # target's, the pinned half of the contract is unverifiable and the
            # answer is HOLD, not OK.
            holds.append(
                f"OBJECT-FORMAT: the manifest pins {pinned_fmt} but the "
                f"target's object format cannot be determined ({repo} is not a "
                f"repository, or git could not report it); the mode and oid "
                f"comparisons cannot run, so gate integrity is unverified")
        elif live_fmt != pinned_fmt:
            holds.append(
                f"OBJECT-FORMAT: target is {live_fmt}, manifest pins "
                f"{pinned_fmt} — refusing to compare object ids across formats")
        else:
            try:
                live_blobs = _tree_blobs(repo)
            except RuntimeError as exc:
                holds.append(f"OBJECT-FORMAT: {exc}")

    for rel, entry in pinned_frozen.items():
        pinned_sha = _entry_sha256(entry)
        if rel not in current_frozen:
            holds.append(f"FROZEN-MISSING: {rel} (a pinned gate file was removed)")
            continue
        if current_frozen[rel] != pinned_sha:
            holds.append(f"FROZEN-MODIFIED: {rel} (gate file edited — sha differs)")
        if isinstance(entry, dict) and live_blobs:
            live = live_blobs.get(rel)
            if live is None:
                holds.append(
                    f"FROZEN-UNTRACKED: {rel} (pinned but not tracked at HEAD — "
                    f"code that can affect collection or execution must be "
                    f"bound to a commit)")
            else:
                live_mode, live_oid = live
                if live_mode != entry.get("mode"):
                    holds.append(
                        f"FROZEN-MODE: {rel} ({entry.get('mode')} -> {live_mode})")
                if live_oid != entry.get("oid"):
                    holds.append(
                        f"FROZEN-OID: {rel} (git object id differs from the "
                        f"pinned one)")
    for rel in sorted(set(current_frozen) - set(pinned_frozen)):
        if live_blobs and rel not in live_blobs:
            # R1-C asks for a HOLD here.  It is scoped to the ceremony mode,
            # and the reason is measured rather than assumed: **v1 never held
            # on untracked gate files** -- it emitted `FROZEN-NEW` for any new
            # path, tracked or not (see the pre-change `verify`).  R1-C lists
            # the untracked HOLD under "the behavioral contract stays", but it
            # is a NEW strictness, not a preserved one.
            #
            # Applied unconditionally it reds the gate for anyone holding an
            # untracked test file, which in a live multi-agent tree is
            # continuous -- a permanently-red gate people learn to ignore.
            # "Bound to a commit" is load-bearing at the **ceremony**, where
            # the pin becomes authoritative and the tree is clean; interactive
            # verification gets the fact as a note.
            msg = (f"{rel} (a gate file under a frozen root is not tracked at "
                   f"HEAD — code that can affect collection or execution must "
                   f"be bound to a commit)")
            if require_anchor:
                holds.append(f"FROZEN-UNTRACKED: {msg}")
            else:
                notes.append(f"FROZEN-UNTRACKED: {msg} [note: ceremony mode "
                             f"(--require-anchor) makes this a HOLD]")
        else:
            notes.append(
                f"FROZEN-NEW: {rel} (new tracked gate/test file — allowed, "
                f"joins the next checkpoint)")

    # 4) Collection identity — dropped node or new skip/xfail HOLDs; added recorded.
    pinned_ids = set(manifest["collection"]["node_ids"])
    if do_collect:
        collected, marked, rc = _collect(repo)
        if rc != 0:
            holds.append(f"COLLECTION: pytest collection failed (rc={rc})")
        cur_ids = set(collected)
        for nid in sorted(pinned_ids - cur_ids):
            holds.append(f"COLLECTION-DROPPED: {nid} (reduced test collection)")
        pinned_marked = set(manifest["collection"]["skip_xfail_marked"])
        for nid in sorted(set(marked) - pinned_marked):
            holds.append(f"SKIP-XFAIL-NEW: {nid} (a test gained a skip/xfail marker)")
        for nid in sorted(cur_ids - pinned_ids):
            notes.append(f"COLLECTION-ADDED: {nid} (new test — allowed, recorded)")
    else:
        notes.append("COLLECTION: skipped (static-only verification, --no-collect)")

    # 5) Cascade-mutable + phase-mutable + mapping digests — report deltas, never HOLD.
    for rel, info in manifest["cascade_mutable"].items():
        cur = _sha256(repo / rel) if (repo / rel).is_file() else "<absent>"
        if cur != info["pre_run_sha256"]:
            notes.append(f"CASCADE-CHANGED: {rel} (governed by: {info['governed_by']})")
    for rel, info in manifest.get("phase_mutable", {}).items():
        cur = _sha256(repo / rel) if (repo / rel).is_file() else "<absent>"
        if cur != info["pre_run_sha256"]:
            notes.append(f"PHASE-CHANGED: {rel} (governed by: {info['governed_by']})")
    baseline_p = repo / "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
    if baseline_p.is_file():
        baseline = json.loads(baseline_p.read_text(encoding="utf-8"))
        for sym, info in manifest["mapping_symbols"].items():
            cur = baseline.get(f"Assign:{sym}", {}).get("digest")
            if cur != info["baseline_digest"]:
                notes.append(f"MAPPING-DIGEST-CHANGED: {sym} {info['baseline_digest']} -> "
                             f"{cur} (allowed phases: {', '.join(info['may_change_in_phases'])})")

    for n in notes:
        print(f"[gate-manifest] note: {n}", file=out)
    if holds:
        print(f"[gate-manifest] HOLD — {len(holds)} gate-integrity violation(s):", file=out)
        for h in holds:
            print(f"  {h}", file=out)
        return 1
    print(f"[gate-manifest] OK — gate integrity intact "
          f"({len(pinned_frozen)} frozen files, {len(pinned_ids)} pinned nodes, "
          f"{len(notes)} note(s))", file=out)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gate_manifest", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("produce", help="emit the gate-integrity manifest JSON to stdout")
    v = sub.add_parser("verify", help="verify gate integrity against a manifest")
    v.add_argument("--target-repo", default=None,
                   help="the tree to verify (the batch worktree); this trusted tool's CODE "
                        "still runs from wherever it is invoked. Defaults to this checkout.")
    v.add_argument("--manifest", default=None,
                   help="manifest path (defaults to <target-repo>/" + _MANIFEST_REL + ")")
    v.add_argument("--anchor-ref", default=None,
                   help="FULL git sha holding the immutable manifest (the prerequisite commit)")
    v.add_argument("--require-anchor", action="store_true",
                   help="HOLD if no --anchor-ref is supplied (unattended verification mode)")
    v.add_argument("--trusted-repo", default=None,
                   help="resolve the anchor manifest object from THIS repo (not the "
                        "target) and require --anchor-ref reachable from --trusted-ref "
                        "here — the external anchor (Codex cross-phase #1).")
    v.add_argument("--trusted-ref", default="HEAD",
                   help="the trusted ref --anchor-ref must be reachable from in "
                        "--trusted-repo (default: HEAD).")
    v.add_argument("--no-collect", action="store_true",
                   help="skip the pytest collection check (static-only)")
    args = ap.parse_args(argv)
    if args.cmd == "produce":
        json.dump(produce(), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    target = Path(args.target_repo) if args.target_repo else _REPO
    manifest = args.manifest if args.manifest else str(target / _MANIFEST_REL)
    return verify(manifest, anchor_ref=args.anchor_ref, repo=target,
                  require_anchor=args.require_anchor, do_collect=not args.no_collect,
                  trusted_repo=args.trusted_repo, trusted_ref=args.trusted_ref)


if __name__ == "__main__":
    raise SystemExit(main())
