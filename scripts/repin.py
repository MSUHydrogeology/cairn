#!/usr/bin/env python3
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
# SPDX-License-Identifier: MIT
"""Re-pin checksums and re-anchor the gate, as one command a person runs.

``status`` reads and writes nothing: it shows what the engine's AST pin and
the gate manifest owe, and which commits touched the files involved.
``packet`` writes the authorization packet and the launcher for an ordinary
ceremony into ``--ceremony-dir``, from the anchor's own launcher template; a
ceremony that changes an authority file is built by hand and this refuses it.
``package`` computes the AST pin's transaction (the new baseline bytes, and the
known-new file when it must change), prints its digest and writes only into
``--ceremony-dir``.  The write itself, ``apply_pin``, never commits: it stops
after one ``yes`` and prints the ``git commit`` line.  ``ceremony`` runs the
whole re-anchor at a terminal: it compares the launcher's digest, checks the
packet, the launcher against the anchor's template, the committed record,
the roster and the anchor signature, refuses a signing key that is loaded in any
agent or stored without a passphrase, writes an owed AST pin and stops, or runs
the launcher's two stages, asks you to read two summaries and verifies the
signature it gets.  The only secret is the passphrase you type at the signer's
own prompt; this tool never reads it.  It never pushes.  Nothing runs this
unprompted.

Every check reads the committed tree (``HEAD``), never the working tree: the
files are extracted from raw git objects, the code this process runs is
compared byte for byte with the signed anchor's manifest before it is
imported, the ten listed files are loaded by file location and the extraction is
never on the import path, and the process itself runs isolated (``-I``) with a
fresh bytecode folder.  A same-user edit to this file is outside what it can detect.
"""
import os
import sys
import tempfile

if __name__ == "__main__":
    if not sys.flags.isolated:
        os.execv(sys.executable,
                 [sys.executable, "-I", os.path.abspath(__file__), *sys.argv[1:]])
    import tempfile
    sys.pycache_prefix = tempfile.mkdtemp(prefix="repin-pyc-")

import argparse
import ast
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import re
import secrets
import shutil
import stat
import subprocess
import sysconfig
import tempfile
import types
import unicodedata
from pathlib import Path

ANCHOR_REF = "refs/cairn/gate-anchor"
MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
REPIN_REL = "scripts/repin.py"
RUNBOOK = "bootstrap/REANCHOR_RUNBOOK.md"
#: Files whose bytes must equal the anchor's before anything is imported: the
#: modules this process imports (the seven `_gate_preflight` loads and their
#: package marker), the AST child's module and the driver.  `repin.py` is the
#: running file and is judged separately.
LISTED = ["bootstrap/tests/__init__.py", "bootstrap/tests/_ast_attest.py",
          "bootstrap/tests/_gate_manifest.py", "bootstrap/tests/_gate_preflight.py",
          "bootstrap/tests/_gate_reanchor.py", "bootstrap/tests/_gate_transition.py",
          "bootstrap/tests/_oracle.py", "bootstrap/tests/_oracle_activation.py",
          "bootstrap/tests/_oracle_trust.py", "scripts/reanchor_ceremony.py"]
BASELINE_REL = "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
KNOWN_NEW_REL = "bootstrap/tests/fixtures/scaffold_ast_known_new.json"
VERIFIER_REL = "bootstrap/tests/_gate_manifest.py"
VERIFIER_SCANNER_PATHS = [
    "bootstrap/tests/__init__.py", "bootstrap/tests/_gate_manifest.py",
    "bootstrap/tests/_gate_preflight.py", "bootstrap/tests/_gate_reanchor.py",
    "bootstrap/tests/_gate_transition.py", "bootstrap/tests/_oracle.py",
    "bootstrap/tests/_oracle_activation.py", "bootstrap/tests/_oracle_trust.py",
    "scripts/reanchor_ceremony.py",
]
VERIFIER_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
VERIFIER_PACKET = "verifier-evidence.json"
OBSERVER_SOURCE = '''import importlib.util, json, os, sys
from pathlib import Path
capture, nonce, prior, candidate, tool, *args = sys.argv[1:]
spec = importlib.util.spec_from_file_location("prior_gate_manifest", tool)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original_collect = module._collect
calls = []
def collect(repo):
    result = original_collect(repo)
    calls.append((repo, result))
    return result
module._collect = collect
sys.argv = [tool, *args]
exit_code = module.main()
if len(calls) != 1:
    raise SystemExit(81)
if type(exit_code) is not int:
    raise SystemExit(82)
repo, result = calls[0]
envelope = json.dumps({"nonce": nonce, "prior_anchor": prior, "candidate": candidate,
    "target_repo": str(repo), "call_count": len(calls), "exit": result[2],
    "verifier_exit": exit_code,
    "node_ids": result[0], "skip_xfail_marked": result[1]}, sort_keys=True).encode()
fd = os.open(capture, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "wb") as stream:
    stream.write(envelope)
raise SystemExit(exit_code)
'''


class Refuse(Exception):
    """A check failed.  The text says what happened, why, and what to do next."""


D = None  # the anchor's encode_display, loaded once the anchor is read


def d(value):
    """Text from git, files or children, made safe for a terminal."""
    if D is None:
        # Pre-boot verifier preparation must not import candidate code merely to
        # get the anchor's encoder. Escape the text until P has been authenticated.
        return (value if isinstance(value, str) else
                bytes(value).decode("utf-8", "surrogateescape")).encode(
                    "unicode_escape").decode("ascii")
    return D(value if isinstance(value, str)
             else bytes(value).decode("utf-8", "surrogateescape"))


def say(*parts):
    print(*parts, flush=True)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


GIT = shutil.which("git") or "git"
_GIT_FLAGS = ["--no-replace-objects", "-c", "core.useReplaceRefs=false",
              "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
              "-c", "core.quotePath=false", "-c", "core.pager=cat"]


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0", LC_ALL="C",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return env


def git(repo, *args, input=None, check=True):
    """Run git without the caller's configuration; bytes out, None on failure."""
    r = subprocess.run([GIT, "-C", str(repo), *_GIT_FLAGS, *args], input=input,
                       capture_output=True, env=git_env(), check=False)
    if r.returncode == 0:
        return r.stdout
    if check:
        raise Refuse(f"git {args[0]} failed (exit {r.returncode})"
                     + (f": {d(r.stderr.strip())}" if D else "")
                     + ". Nothing was written. Fix the repository, then run again.")
    return None


def git_text(repo, *args):
    return git(repo, *args).decode().strip()


# ---------------------------------------------------------------------------
# the reading order: resolve, read the anchor as data, extract, compare, import
# ---------------------------------------------------------------------------

def load_encoder(repo, anchor, tmp):
    """The one terminal encoder, from the anchor's tree: HEAD's copy never runs."""
    spec = f"{anchor}:tools/session.py"
    oid = git(repo, "rev-parse", "--verify", spec, check=False)
    blob = git(repo, "cat-file", "blob", spec, check=False)
    if oid is None or blob is None:
        raise Refuse("the anchor's tree has no tools/session.py, the source of the "
                     "display encoder. Nothing was written. Ask the Maintainer.")
    path = tmp / "anchor-session" / "session.py"
    path.parent.mkdir()
    path.write_bytes(blob)
    if sha(path.read_bytes()) != sha(blob):
        raise Refuse("the extracted encoder module differs from the anchor's blob.")
    spec_ = importlib.util.spec_from_file_location("anchor_session", path)
    mod = importlib.util.module_from_spec(spec_)
    sys.modules["anchor_session"] = mod
    spec_.loader.exec_module(mod)
    if not hasattr(mod, "encode_display"):
        raise Refuse("the anchor's tools/session.py has no encode_display.")
    return mod.encode_display, oid.decode().strip(), path


def cat_blobs(repo, oids):
    raw = git(repo, "cat-file", "--batch", input="".join(o + "\n" for o in oids).encode())
    out, pos = {}, 0
    for oid in oids:
        end = raw.index(b"\n", pos)
        name, kind, size = raw[pos:end].split()
        if name.decode() != oid or kind != b"blob":
            raise Refuse(f"git cat-file returned something other than blob {oid}.")
        out[oid] = raw[end + 1:end + 1 + int(size)]
        pos = end + 1 + int(size) + 1
    return out


def extract(repo, head, dest):
    """Write HEAD's tracked files into dest from raw objects.

    Not ``git archive``: it obeys a tracked ``.gitattributes`` (``export-ignore``
    drops a file, ``export-subst`` rewrites one).  Refuses symlinks, submodules,
    tracked compiled files, names equal after case-folding or normalisation and
    any path that would land outside ``dest``.
    """
    ents, seen = [], {}
    for rec in git(repo, "ls-tree", "-r", "-z", "--full-tree", head).split(b"\0"):
        if not rec:
            continue
        meta, _, raw = rec.partition(b"\t")
        mode, _, oid = meta.decode().split()
        path = raw.decode("utf-8", "surrogateescape")
        parts = path.split("/")
        key = unicodedata.normalize("NFD", unicodedata.normalize("NFD", path).casefold())
        if mode not in ("100644", "100755"):
            raise Refuse(f"the tree holds a symlink or submodule (mode {mode}) at "
                         f"{d(path)}. Remove it from the commit, then run again.")
        if any(p in ("", ".", "..") or p.lower() == ".git" for p in parts):
            raise Refuse(f"the tree holds the unusable path {d(path)}.")
        if path.endswith(".pyc") or "__pycache__" in parts:
            raise Refuse(f"a compiled file is tracked: {d(path)}. Python would run it "
                         f"in place of its source. Remove it from the commit.")
        if key in seen:
            raise Refuse(f"{d(path)} and {d(seen[key])} are one name on a "
                         f"case-insensitive disk. Rename one in a new commit.")
        seen[key] = path
        ents.append((mode, oid, path))
    if not ents:
        raise Refuse("HEAD tracks no files, so there is nothing to read.")
    blobs, root = cat_blobs(repo, [e[1] for e in ents]), dest.resolve()
    for _mode, oid, path in ents:
        target = root.joinpath(*path.split("/"))
        if root not in target.resolve().parents:
            raise Refuse(f"{d(path)} would be written outside the extraction folder.")
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "xb") as fh:
            fh.write(blobs[oid])
        if sha(target.read_bytes()) != sha(blobs[oid]):
            raise Refuse(f"{d(path)} read back from disk differs from its blob.")
    return ents


def baseline_prepare(repo, candidate, approved_roster, reader_record, output_dir):
    """Prepare a no-predecessor baseline package from one committed candidate.

    The approved roster and reader record are inputs from outside the candidate.
    Candidate code is collected only in an extracted tree with an allowlisted
    environment; it never receives the caller's signing credentials. This
    command prepares evidence only and cannot sign or move a ref.
    """
    repo = Path(repo).resolve()
    candidate = git_text(repo, "rev-parse", "--verify", candidate + "^{commit}")
    if git(repo, "cat-file", "blob", f"{candidate}:{REPIN_REL}", check=False) != Path(__file__).read_bytes():
        raise Refuse("running scripts/repin.py differs from the committed candidate; commit and review it first.")
    output = _plain_absolute_path(output_dir)
    parent = output.parent
    if output.exists() or output.is_symlink() or parent.is_symlink() or not parent.is_dir():
        raise Refuse("baseline package path must be new, with an existing plain parent.")
    roster_path = _plain_absolute_path(approved_roster)
    reader_path = _plain_absolute_path(reader_record)
    for path in (roster_path, reader_path):
        if path.is_symlink() or not path.is_file():
            raise Refuse("independent approved roster and reader record must be plain files.")
        if path == repo or repo in path.parents:
            raise Refuse("approved roster and reader record must be supplied outside the candidate checkout.")
    if output == repo or repo in output.parents:
        raise Refuse("baseline package must be written outside the candidate checkout.")
    roster_raw = roster_path.read_bytes()
    reader_raw = reader_path.read_bytes()
    reader = _unique_json(reader_raw, "baseline reader record")
    if (not isinstance(reader, dict)
            or reader.get("schema") != "cairn-baseline-reader/v1"
            or reader.get("candidate") != candidate
            or reader.get("roster_sha256") != sha(roster_raw)
            or not isinstance(reader.get("reviewer"), str) or not reader["reviewer"].strip()
            or reader.get("reviewed") is not True):
        raise Refuse("independent reader record is missing, malformed, or bound to different inputs.")

    temp = Path(tempfile.mkdtemp(prefix="repin-baseline-"))
    try:
        extracted = temp / "candidate"
        ents = extract(repo, candidate, extracted)
        required = baseline_required_paths()
        paths = {path for _mode, _oid, path in ents}
        sys.path.insert(0, str(extracted))
        try:
            import importlib
            gm = importlib.import_module("bootstrap.tests._gate_manifest")
            gp = importlib.import_module("bootstrap.tests._gate_preflight")
            approved = gm._roster_from_bytes(roster_raw, require_initial_approval=True)
            if not required.issubset(paths):
                raise Refuse("candidate is missing required baseline or authority files: "
                             + ", ".join(sorted(required - paths)))
            if approved["path"] not in required or git(
                    repo, "cat-file", "blob", f"{candidate}:{approved['path']}",
                    check=False) != roster_raw:
                raise Refuse("candidate roster differs from the independently supplied approved roster.")
        except (OSError, RuntimeError, ValueError, KeyError, ImportError) as exc:
            if isinstance(exc, Refuse):
                raise
            raise Refuse(f"independent approved roster is invalid: {exc}") from None
        engine = sorted(p for _m, _o, p in ents
                        if re.fullmatch(r"bootstrap/_scaffold/[^/]+\.py", p))
        probe_ctx = {"repo": repo, "head": candidate, "anchor": "no-signed-predecessor",
                     "ext": extracted, "tmp": temp, "engine": engine, "ents": ents,
                     "closure_changed": [], "baseline_mode": True,
                     "session_oid": git_text(repo, "rev-parse",
                                              f"{candidate}:tools/session.py")}
        transaction = build_transaction(probe_ctx, baseline=True)
        if transaction is not None:
            raise Refuse("candidate still owes reviewed AST or lockfile preparation. Complete and "
                         "commit those changes before preparing the final baseline package.")
        # Load the candidate's manifest producer and independent static checker
        # from the extracted candidate, then compare their derived static fields.
        try:
            manifest = gm.produce(extracted, protected_roster=approved)
            static = gp.rederive_static_manifest(candidate, protected_roster=approved, repo=repo)
            if manifest.get("collection", {}).get("node_ids") == []:
                raise Refuse("candidate collection is empty.")
            manifest = gp.authoritative_manifest(manifest, static)
        except (OSError, RuntimeError, ValueError, KeyError, ImportError) as exc:
            if isinstance(exc, Refuse):
                raise
            raise Refuse(f"candidate static derivation failed: {exc}") from None
        finally:
            if sys.path and sys.path[0] == str(extracted):
                sys.path.pop(0)
        raw_manifest = dump(manifest)
        # Bind the program that prepares and installs this baseline too. The
        # reader's record is a review of the whole execution path, not just the
        # shared checker modules.
        tool_hashes = {p: sha(git(repo, "cat-file", "blob", f"{candidate}:{p}"))
                       for p in sorted(required) if p.endswith(".py") or p in
                       (RUNBOOK, "bootstrap/reanchor.sh", "bootstrap/reanchor-launcher.template.sh",
                        "dev/.cairn/allowed_signers")}
        package = {"schema": "cairn-baseline-package/v1", "candidate": candidate,
                   "candidate_tree_sha256": _candidate_tree_digest(repo, candidate),
                   "roster_sha256": sha(roster_raw), "manifest_sha256": sha(raw_manifest),
                   "collection_sha256": sha(dump({"node_ids": manifest["collection"]["node_ids"],
                                                   "skip_xfail_marked": manifest["collection"]["skip_xfail_marked"]})),
                   "interpreter": sys.version.split()[0], "python": os.path.realpath(sys.executable),
                   "python_sha256": sha(Path(os.path.realpath(sys.executable)).read_bytes()),
                   "tool_hashes": tool_hashes, "reader_record_sha256": sha(reader_raw),
                   "reader_record": str(reader_path), "old_anchor_id": (
                       git(repo, "rev-parse", "--verify", ANCHOR_REF + "^{commit}",
                           check=False) or b"missing").decode().strip()}
        packet = dump(package)
        baseline_ctx = {"repo": repo, "head": candidate, "baseline": package,
                        "baseline_manifest": raw_manifest}
        check_record(baseline_ctx, sha(packet), package["reader_record_sha256"],
                     baseline_record=reader_path)
        build_packet(baseline_ctx, output, baseline=True)
        say(f"prepared baseline package for candidate {candidate}; no authority changed")
        say(f"manifest {sha(raw_manifest)}; collection {manifest['collection']['node_count']} nodes; "
            f"reader record {sha(reader_raw)}")
        return package
    finally:
        shutil.rmtree(temp, ignore_errors=True)


def ctx_baseline_tool_paths():
    """The independent derivation and manifest producer used for preparation."""
    return ["bootstrap/tests/_gate_manifest.py", "bootstrap/tests/_gate_preflight.py"]


def baseline_required_paths():
    """Closed candidate input set used by both reader preparation and packaging."""
    return {"bootstrap/tests/fixtures/protected_test_roster.json",
            MANIFEST_REL, REPIN_REL, RUNBOOK, "dev/.cairn/allowed_signers", "tools/session.py",
            "bootstrap/reanchor.sh", "bootstrap/reanchor-launcher.template.sh",
            *LISTED, *ctx_baseline_tool_paths()}


def baseline_reader_inputs(repo, candidate, approved_roster, output):
    """Write a reviewer-editable record draft bound to independently derived C1 inputs."""
    repo = _plain_absolute_path(repo)
    candidate = git_text(repo, "rev-parse", "--verify", candidate + "^{commit}")
    if git(repo, "cat-file", "blob", f"{candidate}:{REPIN_REL}") != Path(__file__).read_bytes():
        raise Refuse("running reader-input tool differs from scripts/repin.py at the committed candidate.")
    roster_path, output_path = _plain_absolute_path(approved_roster), _plain_absolute_path(output)
    if (roster_path.is_symlink() or not roster_path.is_file()
            or output_path.exists() or output_path.is_symlink() or output_path.parent.is_symlink()
            or not output_path.parent.is_dir()):
        raise Refuse("approved roster must be a plain file and reader draft must be a new file in a plain folder.")
    if any(path == repo or repo in path.parents for path in (roster_path, output_path)):
        raise Refuse("approved roster and reader draft must be outside the candidate checkout.")
    roster_raw = roster_path.read_bytes()
    tmp = Path(tempfile.mkdtemp(prefix="repin-baseline-reader-"))
    try:
        extracted = tmp / "candidate"
        ents = extract(repo, candidate, extracted)
        required = baseline_required_paths()
        paths = {path for _mode, _oid, path in ents}
        if not required.issubset(paths):
            raise Refuse("candidate is missing required baseline or authority files: "
                         + ", ".join(sorted(required - paths)))
        sys.path.insert(0, str(extracted))
        try:
            import importlib
            gm = importlib.import_module("bootstrap.tests._gate_manifest")
            gp = importlib.import_module("bootstrap.tests._gate_preflight")
            approved = gm._roster_from_bytes(roster_raw, require_initial_approval=True)
            if (approved["path"] not in required or git(
                    repo, "cat-file", "blob", f"{candidate}:{approved['path']}", check=False) != roster_raw):
                raise Refuse("candidate roster differs from the independently supplied approved roster.")
            engine = sorted(p for _mode, _oid, p in ents
                            if re.fullmatch(r"bootstrap/_scaffold/[^/]+\.py", p))
            transaction = build_transaction(
                {"repo": repo, "head": candidate, "anchor": "no-signed-predecessor",
                 "ext": extracted, "tmp": tmp, "engine": engine, "ents": ents,
                 "closure_changed": [], "baseline_mode": True,
                 "session_oid": git_text(repo, "rev-parse", f"{candidate}:tools/session.py")},
                baseline=True)
            if transaction is not None:
                raise Refuse("candidate still owes reviewed AST or lockfile preparation; commit it before reader review.")
            manifest = gm.produce(extracted, protected_roster=approved)
            static = gp.rederive_static_manifest(candidate, protected_roster=approved, repo=repo)
            if not manifest.get("collection", {}).get("node_ids"):
                raise Refuse("candidate collection is empty.")
            manifest = gp.authoritative_manifest(manifest, static)
        except (OSError, RuntimeError, ValueError, KeyError, ImportError) as exc:
            if isinstance(exc, Refuse):
                raise
            raise Refuse(f"candidate reader inputs could not be derived: {exc}") from None
        finally:
            if sys.path and sys.path[0] == str(extracted):
                sys.path.pop(0)
        manifest_raw = dump(manifest)
        tool_hashes = {p: sha(git(repo, "cat-file", "blob", f"{candidate}:{p}"))
                       for p in sorted(required) if p.endswith(".py") or p in
                       (RUNBOOK, "bootstrap/reanchor.sh", "bootstrap/reanchor-launcher.template.sh",
                        "dev/.cairn/allowed_signers")}
        record = {"schema": "cairn-baseline-reader/v1", "candidate": candidate,
                  "roster_sha256": sha(roster_raw), "manifest_sha256": sha(manifest_raw),
                  "collection_sha256": sha(dump({"node_ids": manifest["collection"]["node_ids"],
                                                   "skip_xfail_marked": manifest["collection"]["skip_xfail_marked"]})),
                  "interpreter": sys.version.split()[0], "tool_hashes": tool_hashes,
                  "reviewer": "", "reviewed": False}
        write_new(output_path, dump(record))
        say(f"wrote unreviewed reader draft {output_path} for candidate {candidate}; "
            "independently verify every field, then fill reviewer and reviewed before preparation")
        return record
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def baseline_install(repo, candidate, package_dir, approved_roster, reader_record,
                     signing_key, expected_fingerprint, confirmed_package_sha256):
    """Install a reviewed baseline package through the existing signed-commit path.

    This is intentionally separate from ``ceremony``: an absent or invalid
    prior anchor never selects it. All package, reader, candidate and signer
    checks happen before the first signing operation. Candidate tests are not
    run here; collection is the reader-bound result prepared in C1.
    """
    repo = _plain_absolute_path(repo)
    candidate = git_text(repo, "rev-parse", "--verify", candidate + "^{commit}")
    if git_text(repo, "rev-parse", "--verify", "HEAD^{commit}") != candidate:
        raise Refuse("baseline installation requires HEAD to be the exact reviewed candidate.")
    if git(repo, "status", "--porcelain", check=False):
        raise Refuse("baseline installation requires a clean candidate worktree and index.")
    if git(repo, "cat-file", "blob", f"{candidate}:{REPIN_REL}") != Path(__file__).read_bytes():
        raise Refuse("running installer differs from scripts/repin.py at the reviewed candidate.")

    package_dir = _plain_absolute_path(package_dir)
    roster_path = _plain_absolute_path(approved_roster)
    reader_path = _plain_absolute_path(reader_record)
    for path in (package_dir, roster_path, reader_path):
        if path == repo or repo in path.parents:
            raise Refuse("package, approved roster and reader record must be outside the checkout.")
    if package_dir.is_symlink() or not package_dir.is_dir():
        raise Refuse("baseline package directory must be a plain directory.")
    if any(path.is_symlink() or not path.is_file() for path in (roster_path, reader_path)):
        raise Refuse("approved roster and reader record must be plain files.")
    package_file, manifest_file = package_dir / "baseline-package.json", package_dir / "gate_manifest.json"
    if any(path.is_symlink() or not path.is_file() for path in (package_file, manifest_file)):
        raise Refuse("baseline package and manifest must be plain files.")
    package_raw, manifest_raw = package_file.read_bytes(), manifest_file.read_bytes()
    if sha(package_raw) != confirmed_package_sha256:
        raise Refuse("baseline package bytes differ from the independently confirmed digest.")
    package = _unique_json(package_raw, "baseline package")
    expected_fields = {"schema", "candidate", "candidate_tree_sha256", "roster_sha256",
                       "manifest_sha256", "collection_sha256", "interpreter", "python",
                       "python_sha256", "tool_hashes", "reader_record_sha256",
                       "reader_record", "old_anchor_id"}
    if (not isinstance(package, dict) or set(package) != expected_fields
            or package.get("schema") != "cairn-baseline-package/v1"):
        raise Refuse("baseline package has an unknown schema or fields.")
    roster_raw, reader_raw = roster_path.read_bytes(), reader_path.read_bytes()
    if (len(package_raw) > 8 * 1024 * 1024 or len(manifest_raw) > 8 * 1024 * 1024
            or len(roster_raw) > 2 * 1024 * 1024 or len(reader_raw) > 2 * 1024 * 1024
            or not isinstance(package.get("tool_hashes"), dict)
            or not package["tool_hashes"]
            or any(not isinstance(k, str) or not isinstance(v, str)
                   or not re.fullmatch(r"[0-9a-f]{64}", v)
                   for k, v in package["tool_hashes"].items())
            or not re.fullmatch(r"[0-9a-f]{64}", confirmed_package_sha256 or "")):
        raise Refuse("baseline package or independent inputs are malformed or exceed their size limits.")
    if (package["candidate"] != candidate
            or package["candidate_tree_sha256"] != _candidate_tree_digest(repo, candidate)
            or package["roster_sha256"] != sha(roster_raw)
            or package["manifest_sha256"] != sha(manifest_raw)
            or package["reader_record_sha256"] != sha(reader_raw)
            or package["reader_record"] != str(reader_path)
            or package["interpreter"] != sys.version.split()[0]
            or package["python"] != os.path.realpath(sys.executable)
            or package["python_sha256"] != sha(Path(os.path.realpath(sys.executable)).read_bytes())):
        raise Refuse("baseline package is stale or mismatched against candidate, roster, reader, or interpreter.")
    manifest = _unique_json(manifest_raw, "baseline manifest")
    if not isinstance(manifest, dict):
        raise Refuse("baseline manifest is not a JSON object.")
    if sha(dump({"node_ids": manifest.get("collection", {}).get("node_ids"),
                 "skip_xfail_marked": manifest.get("collection", {}).get("skip_xfail_marked")})) != package["collection_sha256"]:
        raise Refuse("baseline package collection digest does not match its manifest.")
    if not re.fullmatch(r"SHA256:[A-Za-z0-9+/]{43}", expected_fingerprint or ""):
        raise Refuse("supply the independently authorized signer fingerprint.")
    reader = _unique_json(reader_raw, "baseline reader record")
    if not isinstance(reader, dict):
        raise Refuse("independent baseline reader record is not a JSON object.")
    expected_reader = {"schema": "cairn-baseline-reader/v1", "candidate": candidate,
                       "roster_sha256": package["roster_sha256"],
                       "manifest_sha256": package["manifest_sha256"],
                       "collection_sha256": package["collection_sha256"],
                       "interpreter": package["interpreter"],
                       "tool_hashes": package["tool_hashes"]}
    if (set(reader) != set(expected_reader) | {"reviewer", "reviewed"}
            or any(reader.get(key) != value for key, value in expected_reader.items())
            or reader.get("reviewed") is not True
            or not isinstance(reader.get("reviewer"), str) or not reader["reviewer"].strip()):
        raise Refuse("independent baseline reader record is missing, malformed or stale.")

    tmp = Path(tempfile.mkdtemp(prefix="repin-baseline-install-"))
    try:
        extracted = tmp / "candidate"
        entries = extract(repo, candidate, extracted)
        paths = {path for _mode, _oid, path in entries}
        if set(package["tool_hashes"]) != set(package["tool_hashes"]).intersection(paths):
            raise Refuse("baseline package tool closure contains a path outside the candidate.")
        for rel, digest in package["tool_hashes"].items():
            if not isinstance(digest, str) or sha((extracted / rel).read_bytes()) != digest:
                raise Refuse(f"candidate execution closure differs from package at {d(rel)}.")
        required_tool_hashes = (set(LISTED) | set(ctx_baseline_tool_paths())
                                | {REPIN_REL, "tools/session.py", "dev/.cairn/allowed_signers"})
        if required_tool_hashes - set(package["tool_hashes"]):
            raise Refuse("baseline package does not bind the complete installer and checker closure.")
        # Imports below come only from the raw-object extraction whose full
        # closure has just been checked. No candidate test module is imported.
        before = set(sys.modules)
        made = {}
        try:
            made = load_listed(extracted, extracted / "tools/session.py")
            check_loaded(before, made, extracted, package["tool_hashes"])
            gm = sys.modules["bootstrap.tests._gate_manifest"]
            gp = sys.modules["bootstrap.tests._gate_preflight"]
            roster = gm._roster_from_bytes(roster_raw, require_initial_approval=True)
            static = gp.rederive_static_manifest(candidate, protected_roster=roster, repo=repo)
            rebuilt = gp.authoritative_manifest(manifest, static)
            if dump(rebuilt) != manifest_raw:
                raise Refuse("baseline manifest static fields do not rederive from the candidate.")
            reader_ctx = {"repo": repo, "head": candidate, "baseline": package}
            check_record(reader_ctx, sha(package_raw), package["reader_record_sha256"],
                         baseline_record=reader_path)
            signer_path, signer_fingerprint = gp.validate_signing_key(signing_key)
            if signer_fingerprint != expected_fingerprint:
                raise Refuse("signing key does not match the independently authorized fingerprint.")
            signer_roster_path = extracted / "dev/.cairn/allowed_signers"
            signer_roster_raw = signer_roster_path.read_bytes()
            public = Path(signer_path).read_text(encoding="utf-8").split()
            if len(public) < 2 or not any(
                    fields[i:i + 2] == public[:2]
                    for line in signer_roster_raw.decode("utf-8").splitlines()
                    for fields in [line.split()] for i in range(max(0, len(fields) - 1))):
                raise Refuse("signing key is not present in the candidate's reader-bound signer roster.")
            principals = gp.parse_principals(signer_roster_raw.decode("utf-8"))
            width = len(git_text(repo, "rev-parse", "--verify", "HEAD^{commit}"))
            observed_anchor = git_text(repo, "rev-parse", "--verify",
                                       ANCHOR_REF + "^{commit}") if git(
                                           repo, "rev-parse", "--verify", ANCHOR_REF + "^{commit}",
                                           check=False) else "0" * width
            branch = git_text(repo, "symbolic-ref", "HEAD")
            if not branch.startswith("refs/heads/") or git_text(repo, "rev-parse", branch) != candidate:
                raise Refuse("baseline install requires the reviewed candidate at the current branch tip.")
            gp._require_direct_ref(branch, repo=repo)
            if git(repo, "rev-parse", "--verify", ANCHOR_REF, check=False):
                gp._require_direct_ref(ANCHOR_REF, repo=repo)
            message = ("Cairn forward trust baseline\n\n"
                       f"Candidate: {candidate}\nCandidate tree SHA-256: {package['candidate_tree_sha256']}\n"
                       f"Manifest SHA-256: {package['manifest_sha256']}\n"
                       f"Approved roster SHA-256: {package['roster_sha256']}\n"
                       f"Reader record SHA-256: {package['reader_record_sha256']}\n"
                       f"Authorized signer: {expected_fingerprint}\n"
                       f"Observed prior anchor: {observed_anchor}\n")
            new, blob = gp._construct_signed_commit(repo, candidate, manifest_raw, message,
                                                     signing_key=signer_path)
            gp.verify_constructed(repo, new, candidate,
                                  manifest_sha256="sha256:" + package["manifest_sha256"], message=message,
                                  principals=principals, roster_path=signer_roster_path,
                                  expected_fingerprint=expected_fingerprint)
            ok, detail = gp._advance_both_refs(repo, branch, new, branch_old=candidate,
                                               anchor_old=observed_anchor)
            if not ok:
                raise Refuse("atomic branch and anchor update refused; neither ref moved: " + detail)
            gp._sync_worktree(repo, manifest_raw, blob)
            say(f"installed reviewed baseline {new}; atomic refs advanced from observed anchor {observed_anchor}")
            return new
        finally:
            for name in reversed([n for n in made if n in sys.modules]):
                del sys.modules[name]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


#: The in-process modules, each after the ones it imports.  The others in LISTED
#: are the empty package marker (loaded first) and the AST child's module.
LOAD = ["bootstrap.tests._oracle_trust", "bootstrap.tests._oracle", "bootstrap.tests._oracle_activation",
        "bootstrap.tests._gate_transition", "bootstrap.tests._gate_manifest",
        "bootstrap.tests._gate_reanchor", "bootstrap.tests._gate_preflight",
        "scripts.reanchor_ceremony"]


def load_listed(ext, session_path):
    """Load the listed modules by file location under their dotted names.

    The extraction never joins ``sys.path``, so nothing else in the commit can be
    found by an import: not a ``bootstrap/__init__.py`` or ``scripts/__init__.py``,
    and not a root ``bootstrap.py`` or ``scripts.py``.  The two parent packages are
    empty ones made here.  Returns each loaded name with the file it came from."""
    made = {"anchor_session": session_path}
    for pkg in ("bootstrap", "scripts"):
        parent = types.ModuleType(pkg)
        parent.__path__, parent.__spec__ = [], importlib.machinery.ModuleSpec(pkg, None, is_package=True)
        sys.modules[pkg] = made[pkg] = parent
    try:
        for name in ["bootstrap.tests", *LOAD]:
            path = ext.joinpath(*name.split(".")) / "__init__.py" if name == "bootstrap.tests" else \
                ext.joinpath(*name.split(".")).with_suffix(".py")
            spec = importlib.util.spec_from_file_location(
                name, path, submodule_search_locations=[] if name == "bootstrap.tests" else None)
            mod = sys.modules[name] = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            setattr(sys.modules[name.rpartition(".")[0]], name.rpartition(".")[2], mod)
            made[name] = path
    except ImportError as exc:
        raise Refuse(f"a checked module imported something outside the checked list ({d(str(exc))}). "
                     f"Nothing further was run.")
    return made


def check_loaded(before, made, ext, frozen):
    """Judge every module this boot added by where the import system loaded it from
    (``__spec__``), never by the module's own ``__file__``, which it can reset."""
    stdlib = [os.path.realpath(sysconfig.get_path(k)) for k in ("stdlib", "platstdlib")]
    for name in sorted(set(sys.modules) - before):
        origin = getattr(getattr(sys.modules[name], "__spec__", None), "origin", None)
        if name in made:
            ours = made[name]
            if isinstance(ours, types.ModuleType):
                ok = sys.modules[name] is ours and origin is None
            else:
                rel = os.path.relpath(ours, ext)
                ok = (origin is not None and os.path.realpath(origin) == os.path.realpath(ours)
                      and (name == "anchor_session" or sha(Path(ours).read_bytes()) == frozen.get(rel)))
            if ok:
                continue
        elif origin in ("built-in", "frozen"):
            continue
        elif origin and "site-packages" not in os.path.realpath(origin) and any(
                os.path.realpath(origin).startswith(s + os.sep) for s in stdlib):
            continue
        raise Refuse(f"the module {name} loaded from {d(str(origin))}, which is not on the "
                     f"checked list. Nothing further was run.")


def boot(repo, tmp, *, prior_authority=False):
    """The reading order.  Returns the context every verb works from."""
    global D
    before = set(sys.modules)
    repo = Path(repo).resolve()
    if Path(git_text(repo, "rev-parse", "--show-toplevel")).resolve() != repo:
        raise Refuse("this script is not inside the top level of its repository.")
    head = git_text(repo, "rev-parse", "--verify", "HEAD^{commit}")
    anchor = git(repo, "rev-parse", "--verify", ANCHOR_REF + "^{commit}", check=False)
    if anchor is None:
        raise Refuse(f"{ANCHOR_REF} does not resolve in this repository. Fetch it: "
                     f"git fetch origin '+{ANCHOR_REF}:{ANCHOR_REF}'")
    anchor = anchor.decode().strip()
    man = json.loads(git(repo, "cat-file", "blob", f"{anchor}:{MANIFEST_REL}"))
    frozen = {k: (v if isinstance(v, str) else v["sha256"])
              for k, v in man.get("frozen_files", {}).items()}
    if not frozen:
        raise Refuse("the anchored manifest lists no frozen files.")
    D, session_oid, session_path = load_encoder(repo, anchor, tmp)
    ext = tmp / "ext"
    ents = extract(repo, head, ext)
    authority = tmp / "authority" if prior_authority else ext
    if prior_authority:
        extract(repo, anchor, authority)
    for rel in LISTED:
        got = sha((authority / rel).read_bytes()) if (authority / rel).is_file() else None
        if got != frozen.get(rel):
            raise Refuse(f"{rel} at HEAD does not equal the anchor's entry "
                         f"({got} against {frozen.get(rel)}). Its bytes decide what "
                         f"this tool runs, so nothing was imported. Only the by-hand "
                         f"ceremony in {RUNBOOK} anchors new bytes.")
    made = load_listed(authority, session_path)
    ctx = {k: sys.modules[v] for k, v in (("gm", "bootstrap.tests._gate_manifest"),
                                          ("gp", "bootstrap.tests._gate_preflight"),
                                          ("rc", "scripts.reanchor_ceremony"))}
    check_loaded(before, made, authority, frozen)
    running = Path(__file__).read_bytes()
    entry = frozen.get(REPIN_REL)
    at_head = (ext / REPIN_REL).read_bytes() if (ext / REPIN_REL).is_file() else None
    state = ("not committed at HEAD" if at_head is None else
             "anchored" if entry == sha(at_head) == sha(running) else
             "no anchored entry" if entry is None else "differs from the anchor")
    ctx.update(repo=repo, tmp=tmp, ext=ext, head=head, anchor=anchor, man=man,
               frozen=frozen, ents=ents, session_oid=session_oid, repin_state=state,
               prior_authority=prior_authority,
               engine=sorted(p for _, _, p in ents if re.fullmatch(
                   r"bootstrap/_scaffold/[^/]+\.py", p)))
    if not ctx["engine"]:
        raise Refuse("HEAD tracks no bootstrap/_scaffold/*.py, so the engine set is empty.")
    # The authority files, from the byte-compared checker; a blob-id difference
    # from the anchor is a transition, which an AST pin never carries.
    members = ctx["gp"].declared_authority_closure()
    ctx["closure"] = members
    ctx["closure_changed"] = [m for m in members if
                              git(repo, "rev-parse", f"{anchor}:{m}", check=False)
                              != git(repo, "rev-parse", f"{head}:{m}", check=False)]
    return ctx


def check_head(ctx):
    now = git_text(ctx["repo"], "rev-parse", "--verify", "HEAD^{commit}")
    if now != ctx["head"]:
        raise Refuse(f"HEAD moved from {ctx['head']} to {now} while this ran. Nothing "
                     f"was written. Run again.")


# ---------------------------------------------------------------------------
# the engine's AST pin: what is owed, and which commits touched it
# ---------------------------------------------------------------------------

_AST_CHILD = r'''
import json, os, sys
root, fx, mods = sys.argv[1], sys.argv[2] + "/", sys.argv[3:]
sys.path.append(root + "/bootstrap/tests")
import _ast_attest as A
base = json.load(open(fx + "scaffold_ast_baseline.json"))
known = json.load(open(fx + "scaffold_ast_known_new.json"))
merged, _ = A._merge_current([root + "/" + m for m in mods])
problems, changed, missing, dup, new = A._classify(base, merged)
rel = lambda p: os.path.relpath(p, root)
fresh = [k for k in new if not A._is_per_module_necessity(k)]
print(json.dumps({
    "isolated": sys.flags.isolated, "prefix": sys.pycache_prefix, "baseline_n": len(base),
    "changed": {k: [v[0], v[1], rel(v[2])] for k, v in changed.items()},
    "spans": {k: A.digest_module(v[2])[k]["span"] for k, v in changed.items()},
    "missing": missing, "dup": dup,
    "new_known": {k: sorted(x for x, _ in merged[k]) for k in fresh},
    "new_files": {k: rel(merged[k][0][1]) for k in fresh}}))
'''


def ast_view(ctx, fixtures=None):
    """Run the AST comparison in a child: isolated, fresh bytecode folder."""
    fixtures = fixtures or ctx["ext"] / Path(BASELINE_REL).parent
    prefix = tempfile.mkdtemp(dir=ctx["tmp"], prefix="pyc-")
    r = subprocess.run([sys.executable, "-I", "-X", f"pycache_prefix={prefix}", "-c",
                        _AST_CHILD, str(ctx["ext"]), str(fixtures), *ctx["engine"]], cwd=ctx["tmp"],
                       env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, capture_output=True)
    if r.returncode:
        raise Refuse(f"the AST comparison failed: {d(r.stderr.strip())}")
    out = json.loads(r.stdout)
    if not out["isolated"] or out["prefix"] != prefix:
        raise Refuse("the AST child did not run isolated with the fresh bytecode folder.")
    old = json.loads((fixtures / Path(KNOWN_NEW_REL).name).read_bytes())
    new = out["new_known"]
    out["rekeyed"] = sorted(k for k in old if k in new and sorted(old[k]) != new[k])
    out["added"] = sorted(set(new) - set(old))
    out["dropped"] = sorted(set(old) - set(new))
    out["owed"] = bool(out["changed"] or out["rekeyed"] or out["added"] or out["dropped"])
    return out


def provenance(ctx, files):
    """The commits since the baseline's last pin that touched *files*, each with
    the plans or proposals its message names.  Shown, never a refusal."""
    repo, head = ctx["repo"], ctx["head"]
    pin = git_text(repo, "log", "-1", "--format=%H", head, "--", BASELINE_REL)
    if not pin or not files:
        return []
    names = {}
    for _m, _o, path in ctx["ents"]:
        if re.fullmatch(r"dev/(plans|proposals)/.+\.md", path) and "_template" not in path:
            stem = path.rsplit("/", 1)[1][:-3]
            slug = re.sub(r"^\d{4}-\d\d-\d\d-[^-]+-", "", stem)
            text = (ctx["ext"] / path).read_text("utf-8", "replace")
            hit = re.search(r"^\*\*Status\*\*:\s*(.+)$", text, re.M)
            names[stem] = (slug, hit.group(1).strip() if hit else "no Status line")
    raw = git(repo, "log", "--format=%H%x1f%s%x1f%b%x1e", f"{pin}..{head}", "--", *sorted(files))
    rows = []
    for rec in raw.decode("utf-8", "surrogateescape").split("\x1e"):
        if not rec.strip("\n"):
            continue
        cid, subject, body = rec.strip("\n").split("\x1f", 2)
        low = (subject + "\n" + body).lower()
        named = [(s, st) for s, (slug, st) in sorted(names.items())
                 if (len(s) >= 6 and s.lower() in low) or (len(slug) >= 6 and slug.lower() in low)]
        rows.append((cid, subject, named))
    return rows


def show_provenance(rows):
    say(f"\nCommits since the last pin that touched those files: {len(rows)}")
    for cid, subject, named in rows:
        say(f"  {cid[:10]}  {d(subject)}")
        for stem, status in named:
            say(f"      the message names `{d(stem)}` (status `{d(status)}`)")
        if not named:
            say("      the message names no plan or proposal")


def first_screen(ctx):
    pin = ctx["man"]["interpreter"]["version_info"]
    gitsha = sha(Path(GIT).read_bytes()) if os.path.isfile(GIT) else "unreadable"
    say(f"HEAD     {ctx['head']}\nanchor   {ctx['anchor']}")
    say(f"git      {d(GIT)}  sha256 {gitsha}")
    say(f"python   {sys.version.split()[0]}  (the anchor pins {pin[0]}.{pin[1]}; "
        f"{'match' if list(sys.version_info[:2]) == pin[:2] else 'DIFFERENT MINOR'})")
    say(f"process  isolated={bool(sys.flags.isolated)}  compiled files go to "
        f"{d(str(sys.pycache_prefix))}")
    source = "the anchor" if ctx["prior_authority"] else "HEAD"
    say(f"checked  {len(LISTED)} files at {source} equal the anchor's entries before any import; "
        f"the display encoder is the anchor's blob {ctx['session_oid']}")
    say(f"repin    {REPIN_REL}: {ctx['repin_state']}")
    changed = ctx["closure_changed"]
    say(f"closure  {len(changed)} of {len(ctx['closure'])} authority files differ from the anchor"
        + "".join(f"\n           {d(m)}" for m in changed))


def show_ast(ctx, view):
    say(f"\nEngine pin (AST attestation), over {len(ctx['engine'])} committed engine modules")
    for k in sorted(view["changed"]):
        old, new, rel = view["changed"][k]
        say(f"  CHANGED  {d(k)}  in {d(rel)}  {old} -> {new}")
    for tag in ("missing", "dup"):
        for k in view[tag]:
            say(f"  {'MISSING' if tag == 'missing' else 'DUPLICATE'}  {d(k)}  (a review item, never a pin)")
    for tag, label in (("rekeyed", "known-new REKEYED"), ("added", "known-new ADDED"),
                       ("dropped", "known-new DROPPED")):
        for k in view[tag]:
            say(f"  {label}  {d(k)}")
    say(f"  AST child isolated={bool(view['isolated'])}, compiled files go to {d(view['prefix'])}")
    say("  pin owed: " + ("yes" if view["owed"] else "no, the baseline accounts for the engine"))
    files = {v[2] for v in view["changed"].values()}
    files |= {view["new_files"][k] for k in view["rekeyed"] + view["added"]}
    show_provenance(provenance(ctx, files))


def manifest_status(ctx, dropped_from=None):
    """Static drift against the anchored manifest.  Collection is not checked."""
    man = {k: v for k, v in ctx["man"].items() if k != "object_format"}
    path = ctx["tmp"] / "anchored-manifest.json"
    path.write_text(json.dumps(man), encoding="utf-8")
    buf = io.StringIO()
    ctx["gm"].verify(path, repo=ctx["ext"], do_collect=False, out=buf)
    lines = [ln.strip() for ln in buf.getvalue().splitlines()]
    say("\nGate manifest drift, by checksum, against the anchored manifest")
    for tag in ("FROZEN-MODIFIED", "FROZEN-MISSING", "FROZEN-NEW"):
        rows = [ln for ln in lines if f"{tag}:" in ln]
        say(f"  {tag}: {len(rows)}")
        for ln in rows:
            say(f"    {d(ln[ln.index(tag):])}")
    for ln in lines:
        if ln and not re.search(r"FROZEN-(MODIFIED|MISSING|NEW)|^\[gate-manifest\]", ln):
            say(f"  other: {d(ln)}")
    say("  This does not check test collection: dropped test nodes appear only in "
        "the full verify run.")
    if dropped_from:
        dropped = re.findall(r"COLLECTION-DROPPED:\s*(\S+)",
                             Path(dropped_from).read_text("utf-8", "replace"))
        kept = [n for n in dropped if (ctx["ext"] / n.split("::")[0]).is_file()]
        say(f"\nDropped test nodes: {len(dropped)}; {len(kept)} sit in a test file "
            f"that still exists (shown first)")
        for n in kept + [n for n in dropped if n not in kept]:
            say(f"  {'file exists  ' if n in kept else 'file missing '}{d(n)}")


# ---------------------------------------------------------------------------
# the AST pin as a transaction, and the one write
# ---------------------------------------------------------------------------

#: The only paths `repin` ever writes.  The gate manifest is not among them: its
#: writer is the signed ceremony, so no transaction can reach it.
LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"
OUTPUTS = (BASELINE_REL, KNOWN_NEW_REL, LOCKFILE_REL)
TXN_NAME = "ast-pin-transaction.json"
STOP_PREFIX = "ast-pin-stop-"


def dump(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()


def split_lockfile(raw):
    """The comment header (kept byte for byte) and the JSON body of the lockfile."""
    lines = raw.decode().split("\n")
    n = next((i for i, ln in enumerate(lines) if ln.strip() and not ln.startswith("#")), len(lines))
    return "\n".join(lines[:n]), json.loads("\n".join(lines[n:]))


def parse_output(rel, raw):
    """An output as a flat dict, so old and new can be compared key by key."""
    if rel != LOCKFILE_REL:
        return json.loads(raw)
    header, doc = split_lockfile(raw)
    return {**{r["dst"]: r for r in doc["files"]},
            "(other fields)": {**{k: v for k, v in doc.items() if k != "files"}, "header": header}}


def lockfile_correction(ctx):
    """The install lockfile with stale records dropped and missing verbatim records added,
    or None.  The mappings are read from config.py at HEAD with ast and never imported."""
    tracked = {p for _m, _o, p in ctx["ents"]}
    if LOCKFILE_REL not in tracked:
        return None
    ext = ctx["ext"]
    header, doc = split_lockfile((ext / LOCKFILE_REL).read_bytes())
    mappings = ()
    if "bootstrap/_scaffold/config.py" in tracked:
        for node in ast.parse((ext / "bootstrap/_scaffold/config.py").read_bytes()).body:
            target = node.targets[0] if isinstance(node, ast.Assign) else getattr(node, "target", None)
            if getattr(target, "id", "") == "_SKILLS_MAPPINGS":
                mappings = ast.literal_eval(node.value)
    kept = [r for r in doc["files"] if r.get("dst") in tracked]
    recorded = {r.get("dst") for r in doc["files"]}
    added = []
    for src, dst, verbatim in mappings:
        if not verbatim or dst in recorded or dst not in tracked:
            continue
        if "templates/" + src not in tracked or (ext / "templates" / src).read_bytes() != (ext / dst).read_bytes():
            raise Refuse(f"{d(dst)} is not byte-identical to its template, so a verbatim record would hide a defect.")
        digest = "sha256:" + sha((ext / dst).read_bytes())
        added.append({"base_hash": digest, "dst": dst, "hash": digest, "src": src, "verbatim": True})
    if len(kept) == len(doc["files"]) and not added:
        return None
    doc["files"] = sorted(kept + added, key=lambda r: r.get("dst", ""))
    return (header + "\n" + json.dumps(doc, indent=2, sort_keys=True) + "\n").encode()


def render_changes(rel, old_raw, new_raw, *, reviewed_deletions=()):
    """Every key the write changes, from the bytes on disk against the bytes to be
    written.  Not stored text and not the checker's classifier."""
    old, new = parse_output(rel, old_raw), parse_output(rel, new_raw)
    if rel == BASELINE_REL and (set(old) - set(new) != set(reviewed_deletions) or set(new) - set(old)):
        raise Refuse("the pin would add or drop a baseline key. That is a full "
                     "re-pin, which erases the motion record. Nothing was written.")
    fmt = lambda v: "(absent)" if v is None else json.dumps(v, sort_keys=True)
    return [f"  {Path(rel).name}  {d(k)}:  {d(fmt(old.get(k)))}  ->  {d(fmt(new.get(k)))}"
            for k in sorted(set(old) | set(new)) if old.get(k) != new.get(k)]


def build_transaction(ctx, *, reviewed_deletions=(), baseline=False):
    """The AST pin as data: the new bytes of each output and what they replace.
    None when no pin is owed."""
    if baseline and ctx.get("baseline_mode") is not True:
        raise Refuse("baseline transaction checks require the explicit baseline preparation context.")
    if ctx["closure_changed"] and not baseline:
        raise Refuse("these authority files differ from the anchor: "
                     + ", ".join(d(m) for m in ctx["closure_changed"])
                     + ". That is a transition ceremony, not an AST pin.")
    view = ast_view(ctx)
    deletions = sorted(reviewed_deletions)
    if view["dup"] or sorted(view["missing"]) != deletions:
        raise Refuse("a baselined symbol is missing or defined twice. Name every reviewed deletion "
                     "exactly; duplicates cannot be pinned. Run `status` and read the symbols named.")
    ext, new, files = ctx["ext"], {}, set()
    old = {rel: (ext / rel).read_bytes() for rel in OUTPUTS if (ext / rel).is_file()}
    if view["owed"] or deletions:
        base = json.loads(old[BASELINE_REL])
        for key in deletions:
            del base[key]
        for key, (_old, digest, _file) in view["changed"].items():
            base[key]["digest"], base[key]["span"] = digest, view["spans"][key]
        new[BASELINE_REL] = dump(base)
        if view["rekeyed"] or view["added"] or view["dropped"]:
            new[KNOWN_NEW_REL] = dump(view["new_known"])
        check = ctx["tmp"] / "pinned-fixtures"
        check.mkdir(exist_ok=True)
        for rel in (BASELINE_REL, KNOWN_NEW_REL):
            (check / Path(rel).name).write_bytes(new.get(rel, old[rel]))
        if ast_view(ctx, check)["owed"]:
            raise Refuse("the pin built here would not account for the engine. Nothing was "
                         "written; this is a defect in repin, so tell the Maintainer.")
        files = set(ctx["engine"]) if deletions else set()
        files |= {v[2] for v in view["changed"].values()}
        files |= {view["new_files"][k] for k in view["rekeyed"] + view["added"]}
    lock = lockfile_correction(ctx)
    if lock is not None:
        new[LOCKFILE_REL] = lock
    if not new:
        return None
    return {"schema": "repin-ast-transaction/v1", "head": ctx["head"], "anchor": ctx["anchor"],
            "reviewed_deletions": deletions,
            "influences": {"python": sys.version, "git_version": git_text(ctx["repo"], "--version"),
                           "display_encoder_blob": ctx["session_oid"]},
            "files": sorted(files),
            "outputs": {rel: {"preimage_blob": git_text(ctx["repo"], "rev-parse", f"{ctx['head']}:{rel}"),
                              "preimage_sha256": sha(old[rel]), "new_sha256": sha(raw),
                              "new_text": raw.decode()} for rel, raw in new.items()},
            "summary": [ln for rel, raw in new.items() for ln in render_changes(rel, old[rel], raw, reviewed_deletions=deletions if rel == BASELINE_REL else ())]}


def encode_txn(txn):
    return json.dumps(txn, sort_keys=True, separators=(",", ":")).encode()


# Containment is written here, not imported from bootstrap/_scaffold/_guard.py:
# the AST baseline attests that module, so a pin run must not execute the very
# code whose digest it is about to write.
def read_safe(path, *, own=False):
    """Read a regular file without following a symlink; with own=True, only a file
    this user owns that no one else can write."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise Refuse(f"{d(str(path))} cannot be opened without following a link ({exc.strerror}).")
    with os.fdopen(fd, "rb") as fh:
        st = os.fstat(fh.fileno())
        if not stat.S_ISREG(st.st_mode) or (own and (st.st_uid != os.getuid() or st.st_mode & 0o022)):
            raise Refuse(f"{d(str(path))} is not a plain file that only this user can write.")
        return fh.read()


def plain_folder(cdir):
    cdir = Path(cdir)
    if cdir.is_symlink() or not cdir.is_dir():
        raise Refuse(f"the ceremony folder {d(str(cdir))} is not a plain folder.")
    return cdir


def store_txn(cdir, raw):
    cdir = plain_folder(cdir)
    fd, tmp = tempfile.mkstemp(dir=cdir, prefix=".txn-")
    with os.fdopen(fd, "wb") as fh:
        fh.write(raw)
    os.replace(tmp, cdir / TXN_NAME)
    return cdir / TXN_NAME


def worktree_diff(ctx):
    """Tracked paths whose bytes on disk differ from HEAD's blob.  Hashed with
    hash-object, so the stat cache, a clean filter or an index bit cannot hide one."""
    paths = [p for _m, _o, p in ctx["ents"]]
    if any("\n" in p for p in paths):
        raise Refuse("a tracked path holds a newline, which this check cannot read.")
    gone = {p for p in paths if not os.path.lexists(ctx["repo"] / p)}
    here = [(o, p) for _m, o, p in ctx["ents"] if p not in gone]
    out = git(ctx["repo"], "hash-object", "--no-filters", "--stdin-paths",
              input="".join(p + "\n" for _o, p in here).encode()).decode().split()
    return sorted(gone | {p for (o, p), h in zip(here, out) if o != h})


def check_preconditions(ctx, *, need_terminal=True):
    """Shared by `ceremony` step 2, the apply step and `packet`: refuse unless the tree
    is a clean, committed branch state that git can report on exactly.  `packet` needs
    no terminal: it asks nothing."""
    repo, pin = ctx["repo"], ctx["man"]["interpreter"]["version_info"]
    if need_terminal and not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise Refuse("stdin and stdout must both be a terminal: a pipe cannot answer. "
                     "Run this in a terminal window.")
    if git(repo, "symbolic-ref", "-q", "HEAD", check=False) is None:
        raise Refuse("HEAD is detached. Check out the branch you mean to pin, then run again.")
    if list(sys.version_info[:2]) != pin[:2]:
        raise Refuse(f"this interpreter is {sys.version_info[0]}.{sys.version_info[1]} but the "
                     f"anchor pins {pin[0]}.{pin[1]}; the digests differ across minors.")
    hidden = [e[2:] for e in git(repo, "ls-files", "-v", "-z").decode("utf-8", "replace").split("\0")
              if e and e[0] != "H"]
    if hidden:
        raise Refuse("an index bit hides changes from git status: "
                     + ", ".join(d(h) for h in hidden[:5]) + ". Clear it with "
                     "`git update-index --no-assume-unchanged --no-skip-worktree <path>`.")
    if git(repo, "diff-index", "--cached", "--raw", "-z", "--no-renames", ctx["head"]):
        raise Refuse("the index holds staged changes. Commit or unstage them, then run again.")
    dirty = worktree_diff(ctx)
    if dirty:
        raise Refuse("tracked files differ from HEAD: " + ", ".join(d(p) for p in dirty[:5])
                     + ". Commit or discard those changes, then run again.")


def ask_yes(question):
    """Only the exact word `yes`, typed at a terminal, counts."""
    try:
        return input(f"\n{question}\n  type the word yes to continue, anything else stops: ") == "yes"
    except (EOFError, KeyboardInterrupt):
        return False


def apply_pin(ctx, cdir, raw, *, reviewed_head=None):
    """`ceremony` step 5: write the AST pin this process just packaged, after one yes.
    Never commits.  *raw* is the transaction packaged in this very process."""
    check_preconditions(ctx)
    repo, head = ctx["repo"], ctx["head"]
    if read_safe(Path(cdir) / TXN_NAME, own=True) != raw:
        raise Refuse("the transaction file changed after it was packaged. Nothing was written.")
    txn = json.loads(raw)
    if txn["head"] != (reviewed_head or head) or not txn["outputs"] or not set(txn["outputs"]) <= set(OUTPUTS):
        raise Refuse(f"the transaction names paths outside {', '.join(OUTPUTS)} (the gate "
                     f"manifest is never written here) or another HEAD. Nothing was written.")
    modes, plan = {p: m for m, _o, p in ctx["ents"]}, []
    for rel, o in txn["outputs"].items():
        target = repo / rel
        if (modes.get(rel) not in ("100644", "100755") or target.resolve() != repo / rel
                or not stat.S_ISREG(os.lstat(target).st_mode)):
            raise Refuse(f"{rel} is not a tracked regular file with no link in its path.")
        new = o["new_text"].encode()
        disk = read_safe(target)
        if sha(new) != o["new_sha256"] or sha(disk) != o["preimage_sha256"]:
            raise Refuse(f"{rel} on disk, or its new bytes, differ from the transaction.")
        plan.append((rel, target, disk, new))
    say("\nSummary 1: every key this write changes, from the file on disk against the bytes to be written")
    for rel, _t, disk, new in plan:
        for line in render_changes(rel, disk, new, reviewed_deletions=txn.get("reviewed_deletions", ()) if rel == BASELINE_REL else ()):
            say(line)
    if KNOWN_NEW_REL in txn["outputs"]:
        say("  The known-new file is a frozen gate file: changing it owes a re-anchor ceremony.")
    show_provenance(provenance(ctx, set(txn["files"])))
    if not ask_yes("Write these files?"):
        raise Refuse("no `yes` was typed. Nothing was written.")
    temps, done = [], []
    try:
        for rel, target, _disk, new in plan:
            fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=target.name + ".", suffix=".tmp")
            temps.append(tmp)
            with os.fdopen(fd, "wb") as fh:
                fh.write(new)
                fh.flush()
                os.fsync(fh.fileno())
            os.chmod(tmp, stat.S_IMODE(os.lstat(target).st_mode))
        check_head(ctx)
        if any(read_safe(t) != disk for _r, t, disk, _n in plan):
            raise Refuse("a file changed while you were reading. Nothing was written.")
        for (rel, target, disk, _new), tmp in zip(plan, temps):
            if read_safe(target) != disk:
                raise Refuse("a file changed while it was being replaced.")
            os.replace(tmp, target)
            done.append(rel)
    except (Refuse, OSError) as exc:
        for tmp in temps:
            Path(tmp).unlink(missing_ok=True)
        if done:
            raise Refuse(f"{exc} Already replaced: {', '.join(done)}. Undo with: git restore "
                         f"--source={head} -- {' '.join(done)}")
        raise Refuse(f"{exc} Nothing was written.")
    undo = f"git restore --source={head} -- {' '.join(rel for rel, *_ in plan)}"
    blobs = {rel: git(repo, "hash-object", "--no-filters", "--stdin", input=new).decode().strip()
             for rel, _t, _d, new in plan}
    here = {rel: git(repo, "hash-object", "--no-filters", rel).decode().strip() for rel in blobs}
    if set(worktree_diff(ctx)) != set(blobs) or here != blobs:
        raise Refuse(f"after the write, the files that differ from HEAD are not exactly the ones "
                     f"named, or their bytes differ from those shown. Nothing was run to undo "
                     f"it. To undo: {undo}")
    digest = sha(raw)
    record = Path(cdir) / f"{STOP_PREFIX}{digest[:16]}.json"
    record.write_bytes(dump({"schema": "repin-ast-stop/v1", "head": head, "paths": blobs,
                             "transaction": digest}))
    say(f"\nWritten, not committed. HEAD is still {head}.\n"
        f"Run commit-reviewed-pin --ceremony-dir {d(str(cdir))} to review and commit exactly: "
        + ", ".join(blobs) + f".\nThen prepare fresh ceremony evidence; the re-run check reads {record.name}.")
    return record


def commit_reviewed_pin(ctx, cdir):
    """Commit only the previously approved write after rechecking its stop record."""
    cdir = plain_folder(cdir)
    raw = read_safe(cdir / TXN_NAME, own=True)
    digest = sha(raw)
    record = json.loads(read_safe(cdir / f"{STOP_PREFIX}{digest[:16]}.json", own=True))
    txn = json.loads(raw)
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise Refuse("a terminal is required to authorize the commit.")
    check_record(ctx, sha(read_safe(cdir / PACKET_NAME)), sha(read_safe(cdir / LAUNCHER_NAME)))
    reader = (ctx["ext"] / RECORD_REL).read_text("utf-8")
    if re.findall(r"^ast-transaction-sha256 ([0-9a-f]{64})$", reader, re.M) != [digest]:
        raise Refuse("the reader record does not bind this transaction.")
    if git_text(ctx["repo"], "rev-list", "--parents", "-n", "1", ctx["head"]).split()[1:] != [txn.get("head")]:
        raise Refuse("the reader record is not the sole child of the reviewed commit.")
    paths = record.get("paths")
    if (record.get("schema") != "repin-ast-stop/v1" or record.get("transaction") != digest
            or record.get("head") != ctx["head"] or not isinstance(paths, dict)
            or not paths or set(paths) != set(txn.get("outputs", {}))
            or not set(paths) <= set(OUTPUTS)):
        raise Refuse("the stop record does not bind this transaction and HEAD.")

    def validate():
        check_head(ctx)
        if set(worktree_diff(ctx)) != set(paths):
            raise Refuse("the changed files differ from the stop record; no commit was made.")
        for rel, blob in paths.items():
            target = ctx["repo"] / rel
            if (not os.path.lexists(target) or target.resolve() != target
                    or not stat.S_ISREG(os.lstat(target).st_mode)):
                raise Refuse(f"{rel} is not a regular file without links; no commit was made.")
            data = read_safe(target)
            expected = txn["outputs"][rel]
            if (sha(data) != expected["new_sha256"] or data != expected["new_text"].encode()
                    or git(ctx["repo"], "hash-object", "--no-filters", "--stdin", input=data).decode().strip() != blob):
                raise Refuse(f"{rel} differs from the reviewed write; no commit was made.")

    validate()
    say("Commit exactly these reviewed paths: " + ", ".join(sorted(paths)))
    if not ask_yes("Commit these files?"):
        raise Refuse("no `yes` was typed. No commit was made.")
    validate()
    message = f"AST pin\n\nTransaction: {digest}\nPython: {sys.version.split()[0]}"
    # A commit needs the operator's normal Git identity and hooks. Strip only
    # environment overrides so a global user.name/user.email still works.
    commit_env = git_env()
    commit_env.pop("GIT_CONFIG_GLOBAL")
    commit_env.pop("GIT_CONFIG_NOSYSTEM")
    result = subprocess.run([GIT, "--no-replace-objects", "-c", "core.useReplaceRefs=false",
                             "-C", str(ctx["repo"]), "commit", "-m", message, "--", *sorted(paths)],
                            env=commit_env, capture_output=True, text=True, check=False)
    relay(result.stdout + result.stderr)
    if result.returncode:
        raise Refuse("the exact-path commit failed; inspect the repository before retrying.")
    new = git_text(ctx["repo"], "rev-parse", "HEAD^{commit}")
    parents = git_text(ctx["repo"], "rev-list", "--parents", "-n", "1", new).split()[1:]
    if parents != [record["head"]]:
        raise Refuse("the resulting commit has an unexpected parent; inspect it before proceeding.")
    check_stop_records(dict(ctx, head=new), cdir, False)
    say(f"Committed reviewed pin at {new}; prepare fresh ceremony evidence.")


NOTHING_OWED = "\nNo pin is owed: the baseline accounts for the engine and the lockfile has nothing to correct."


def package(ctx, cdir=None, *, reviewed_deletions=()):
    """The AST pin's transaction, its digest and (with a folder) the file; no repository write."""
    txn = build_transaction(ctx, reviewed_deletions=reviewed_deletions)
    if txn is None:
        say(NOTHING_OWED)
        return None
    raw = encode_txn(txn)
    say("\nAST pin transaction (what a write would change):")
    for line in txn["summary"]:
        say(line)
    if KNOWN_NEW_REL in txn["outputs"]:
        say("  The known-new file is a frozen gate file: changing it owes a re-anchor ceremony.")
    say(f"transaction digest {sha(raw)}")
    if cdir:
        say(f"transaction file   {d(str(store_txn(cdir, raw)))}")
    return raw


# ---------------------------------------------------------------------------
# the ceremony: checks, the AST pin, the launcher's two stages, verification
# ---------------------------------------------------------------------------

KEYGEN, SSHADD, LAUNCHCTL, SH = "/usr/bin/ssh-keygen", "/usr/bin/ssh-add", "/bin/launchctl", "/bin/sh"
CHILD_PATH = "/usr/bin:/bin"
ARTIFACT_REL = "bootstrap/reanchor.sh"
ROSTER_REL = "dev/.cairn/allowed_signers"
TEMPLATE_REL = "bootstrap/reanchor-launcher.template.sh"
#: The launcher template's one slot, filled with the packet's digest.
SLOT = "@PACKET_SHA256@"
PACKET_NAME, LAUNCHER_NAME = "authorization-packet.txt", "reanchor-launcher.sh"
PACKET_SCHEMA = "cairn-authorization-packet/v1"
#: The reader's record, committed on the commit it read as the candidate's tip.
RECORD_REL = "dev/ceremony-record.md"
REPIN_TESTS = ("bootstrap/tests/test_repin.py", "bootstrap/tests/test_repin_ceremony.py")


def launchctl_socket():
    """The agent socket the login session would hand to any process, or None."""
    r = subprocess.run([LAUNCHCTL, "getenv", "SSH_AUTH_SOCK"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, env={"PATH": CHILD_PATH}, check=False)
    return r.stdout.strip() or None if r.returncode == 0 else None


def child(rec, argv, **kw):
    """Run a child this tool starts, with a short environment; record command and exit."""
    kw.setdefault("env", {"PATH": CHILD_PATH, "LC_ALL": "C"})
    kw.setdefault("stdin", subprocess.DEVNULL)
    r = subprocess.run(argv, capture_output=True, text=True, check=False, **kw)
    rec.append(f"ran {' '.join(argv)} -> exit {r.returncode}")
    return r


def relay(text):
    for line in text.splitlines():
        say(d(line))


def confirm(rec, question):
    if not ask_yes(question):
        raise Refuse("no `yes` was typed. Nothing further was run.")
    rec.append(f"yes typed on a terminal: {question}")


def key_fingerprint(rec, pub):
    r = child(rec, [KEYGEN, "-lf", pub])
    found = [t for t in r.stdout.split() if t.startswith("SHA256:")]
    if r.returncode or not found:
        raise Refuse(f"{d(pub)} is not a readable public key.")
    return found[0]


def key_checks(rec, pub, private, fingerprint, launchctl, when):
    """Refuse a key that is loaded in any agent, or stored without a passphrase.
    The passphrase typed at the one prompt is then the only thing that signs."""
    sockets = [s for s in dict.fromkeys([os.environ.get("SSH_AUTH_SOCK"), launchctl()]) if s]
    for sock in sockets:
        r = child(rec, [SSHADD, "-l"], env={"PATH": CHILD_PATH, "SSH_AUTH_SOCK": sock},
                  start_new_session=True)
        if r.returncode == 2:
            say(f"  agent at {d(sock)}: could not ask it ({when}); shown, not refused")
            rec.append(f"agent at {d(sock)} could not be asked ({when})")
        elif r.returncode == 0 and fingerprint in r.stdout:
            raise Refuse(f"the signing key is loaded in an agent ({when}), which would sign with no "
                         f"passphrase. Remove it with:\n  SSH_AUTH_SOCK={d(sock)} {SSHADD} -d {d(pub)}")
    if child(rec, [KEYGEN, "-y", "-P", "", "-f", private], start_new_session=True).returncode == 0:
        raise Refuse(f"the signing key file {d(private)} has no passphrase ({when}). Encrypt it "
                     f"with ssh-keygen -p, then run again.")
    say(f"  key checks ({when}): not in any agent I could ask, and the file is encrypted")


def blob_at(repo, rev, path):
    rows = git(repo, "ls-tree", "-z", rev, "--", path, check=False)
    return rows.split(b"\0")[0].split()[2].decode() if rows else None


def verify_checkpoint(repo, commit, roster, fingerprint):
    """True only for a good signature, checked against *roster*, by *fingerprint*."""
    out = git(repo, "-c", "gpg.format=ssh", "-c", f"gpg.ssh.allowedSignersFile={roster}",
              "-c", f"gpg.ssh.program={KEYGEN}", "-c", f"gpg.program={os.devnull}",
              "-c", f"gpg.openpgp.program={os.devnull}", "-c", f"gpg.x509.program={os.devnull}",
              "log", "-1", "--format=%G?%x00%GK", commit)
    status, _, key = out.decode().strip().partition("\0")
    return status == "G" and key == fingerprint, status, key


def _verifier_prepare(repo, prior, candidate, trusted_ref, expected_fingerprint,
                      evidence_dir):
    """Prepare raw prior tools and a clean candidate worktree for the human verifier.

    This pre-boot path is preparation only. The running repin.py is not treated as
    authenticated authority; the reader independently checks every emitted hash.
    """
    repo = Path(repo).resolve()
    prior = git_text(repo, "rev-parse", "--verify", prior + "^{commit}")
    candidate = git_text(repo, "rev-parse", "--verify", candidate + "^{commit}")
    trusted_ref = git_text(repo, "rev-parse", "--verify", trusted_ref + "^{commit}")
    if git(repo, "merge-base", "--is-ancestor", prior, trusted_ref, check=False) is None:
        raise Refuse(f"prior anchor {prior} is not reachable from trusted ref {trusted_ref}.")
    preparer = Path(__file__).read_bytes()
    candidate_preparer = git(repo, "cat-file", "blob", f"{candidate}:{REPIN_REL}", check=False)
    if candidate_preparer is None or sha(candidate_preparer) != sha(preparer):
        raise Refuse("the preparation script running now does not equal scripts/repin.py at exact candidate C.")
    if not re.fullmatch(r"SHA256:[A-Za-z0-9+/]{43}", expected_fingerprint):
        raise Refuse("supply the independently trusted SHA256 signing fingerprint.")
    roster_raw = git(repo, "cat-file", "blob", f"{prior}:{ROSTER_REL}", check=False)
    manifest_raw = git(repo, "cat-file", "blob", f"{prior}:{MANIFEST_REL}", check=False)
    if roster_raw is None or manifest_raw is None:
        raise Refuse("prior anchor lacks its signer roster or gate manifest.")
    evidence = _plain_absolute_path(evidence_dir)
    parent = evidence.parent
    if (evidence.exists() or evidence.is_symlink() or parent.is_symlink()
            or not parent.is_dir()):
        raise Refuse("evidence path must be new, with an existing plain parent directory.")
    evidence.mkdir()
    evidence = evidence.resolve()
    prior_dir = evidence / "prior"
    prior_dir.mkdir()
    roster_path = prior_dir / "allowed_signers"
    roster_path.write_bytes(roster_raw)
    good, state, signer = verify_checkpoint(repo, prior, roster_path, expected_fingerprint)
    if not good:
        raise Refuse(f"prior signature did not verify against the independent fingerprint "
                     f"({state}, signer {signer!r}, expected {expected_fingerprint}).")
    manifest = json.loads(manifest_raw)
    frozen = manifest.get("frozen_files", {})
    if not frozen:
        raise Refuse("prior manifest has no frozen file map.")
    prior_hashes = {}
    for rel in VERIFIER_SCANNER_PATHS:
        raw = git(repo, "cat-file", "blob", f"{prior}:{rel}", check=False)
        entry = frozen.get(rel)
        pinned = entry if isinstance(entry, str) else entry.get("sha256") if isinstance(entry, dict) else None
        if raw is None or not pinned or sha(raw) != pinned:
            raise Refuse(f"prior verifier dependency {rel} is missing or differs from P's signed manifest.")
        dst = prior_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(raw)
        prior_hashes[rel] = sha(raw)
    manifest_path = prior_dir / "gate_manifest.json"
    manifest_path.write_bytes(manifest_raw)
    prior_hashes[VERIFIER_MANIFEST_REL] = sha(manifest_raw)
    observer_path = evidence / "verifier-observer.py"
    observer_path.write_text(OBSERVER_SOURCE, encoding="utf-8")
    observer_digest = sha(OBSERVER_SOURCE.encode())

    target = evidence / "candidate"
    if target.exists() or target.is_symlink():
        raise Refuse("candidate target already exists; use a new empty evidence folder.")
    git(repo, "clone", "--no-hardlinks", "--no-checkout", str(repo), str(target))
    git(target, "update-ref", ANCHOR_REF, prior)
    git(target, "checkout", "--detach", candidate)
    _assert_candidate_bytes(repo, candidate, target)
    record = {
        "schema": "cairn-prior-verifier-evidence/v1", "trusted_repo": str(repo),
        "trusted_ref": trusted_ref, "prior_anchor": prior, "candidate": candidate,
        "signer_fingerprint": signer, "expected_fingerprint": expected_fingerprint,
        "verifier": VERIFIER_REL, "verifier_sha256": prior_hashes[VERIFIER_REL],
        "manifest_sha256": prior_hashes[VERIFIER_MANIFEST_REL],
        "prior_dependencies": prior_hashes, "target": str(target),
        "target_tree_sha256": _candidate_tree_digest(repo, candidate),
        "observer": str(observer_path), "observer_sha256": observer_digest,
        "preparer_sha256": sha(preparer),
        "python": os.path.realpath(sys.executable),
        "python_sha256": sha(Path(os.path.realpath(sys.executable)).read_bytes()),
        "warning": "This preparer is not P-authenticated authority; the independent reader must verify P, signer provenance, and all hashes.",
    }
    path = evidence / VERIFIER_PACKET
    path.write_bytes(dump(record))
    say(f"prepared  {path}")
    say(f"prior P   {prior}  signer {signer} (expected independently: {expected_fingerprint})")
    say(f"candidate C {candidate}  raw tree {record['target_tree_sha256']}")
    say(f"verifier  sha256 {record['verifier_sha256']}  manifest sha256 {record['manifest_sha256']}")
    say(f"observer  {observer_path}  sha256 {observer_digest}")
    say(f"preparer  scripts/repin.py at C sha256 {record['preparer_sha256']}")
    say("Reader must independently verify P's signed commit, signer provenance, dependency hashes, exact clean C bytes, and the Python path and digest.")
    say("The target contains candidate code. Run the verifier only with the signing key away.")
    return path


def _candidate_tree_digest(repo, commit):
    rows = git(repo, "ls-tree", "-r", "-z", "--full-tree", commit)
    h = hashlib.sha256()
    for row in sorted(x for x in rows.split(b"\0") if x):
        h.update(row + b"\0")
    return h.hexdigest()


def _assert_candidate_bytes(repo, commit, target):
    """Compare the clean worktree against every raw object in C; refuse links."""
    dotgit = target / ".git"
    if dotgit.is_symlink() or not dotgit.is_dir():
        raise Refuse("candidate Git metadata must be its own plain .git directory.")
    actual_gitdir = Path(git_text(target, "rev-parse", "--absolute-git-dir"))
    if _plain_absolute_path(actual_gitdir) != dotgit:
        raise Refuse("candidate Git metadata is not contained in its prepared target.")
    entries = []
    for row in git(repo, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
        if not row:
            continue
        meta, _, name = row.partition(b"\t")
        mode, kind, oid = meta.split()
        rel = name.decode("utf-8", "surrogateescape")
        if mode not in (b"100644", b"100755") or kind != b"blob":
            raise Refuse(f"candidate contains a symlink or submodule at {d(rel)}.")
        entries.append((rel, oid.decode()))
    if not entries:
        raise Refuse("candidate commit has no tracked blobs.")
    for rel, oid in entries:
        path = target.joinpath(*rel.split("/"))
        parents = list(path.parents)
        if path.is_symlink() or any(p.is_symlink() for p in parents if p != target.parent) or not path.is_file():
            raise Refuse(f"candidate worktree is missing a regular file: {d(rel)}.")
        raw = git(repo, "cat-file", "blob", oid)
        if path.read_bytes() != raw:
            raise Refuse(f"candidate worktree bytes differ from raw C object {d(rel)}.")
    # Git status hides ignored files and can trust index flags. Enumerate the
    # filesystem independently so candidate imports see only committed bytes.
    expected_files = {rel for rel, _ in entries}
    expected_dirs = {str(parent) for rel in expected_files
                     for parent in Path(rel).parents if str(parent) != "."}
    for root, dirs, files in os.walk(target, topdown=True, followlinks=False):
        base = Path(root)
        if base == target and ".git" in dirs:
            dirs.remove(".git")
        for name in dirs:
            path = base / name
            rel = path.relative_to(target).as_posix()
            if path.is_symlink() or rel not in expected_dirs:
                raise Refuse(f"candidate has an unexpected directory or link: {d(rel)}.")
        for name in files:
            path = base / name
            rel = path.relative_to(target).as_posix()
            if path.is_symlink() or rel not in expected_files:
                raise Refuse(f"candidate has an unexpected file or link: {d(rel)}.")
    status = git(target, "status", "--porcelain=v1", "--untracked-files=all")
    if status.strip():
        raise Refuse("candidate worktree is not clean before verifier execution: " + d(status.strip()))
    if git_text(target, "rev-parse", "--verify", "HEAD^{commit}") != commit:
        raise Refuse("candidate worktree HEAD no longer equals exact candidate C.")


def _plain_absolute_path(path):
    """Refuse symlinks in every existing component before using a path."""
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise Refuse(f"path has a symlink component: {d(str(part))}.")
    return path


def _verify_collection_report(manifest, collection, report):
    """Prove P's report names every delta in its same-call captured collection."""
    baseline = manifest.get("collection", {})
    old_ids, old_marked = set(baseline.get("node_ids", [])), set(baseline.get("skip_xfail_marked", []))
    live_ids, live_marked = set(collection["node_ids"]), set(collection["skip_xfail_marked"])
    roster = manifest.get("protected_roster")
    protected = set(roster.get("protected_python_paths", [])) if isinstance(roster, dict) else None
    expected = []
    def ordinary(node):
        return protected is not None and node.split("::", 1)[0] not in protected
    for node in sorted(old_ids - live_ids):
        if ordinary(node):
            expected.append(f"COLLECTION-ORDINARY-DROPPED: {node} (ordinary test collection changed)")
        else:
            expected.append(f"COLLECTION-DROPPED: {node} (reduced protected test collection)")
    for node in sorted(live_ids - old_ids):
        expected.append(f"COLLECTION-ADDED: {node} (new test — allowed, recorded)")
    for node in sorted(live_marked - old_marked):
        if ordinary(node):
            expected.append(f"SKIP-XFAIL-ORDINARY: {node} (ordinary marker change)")
        else:
            expected.append(f"SKIP-XFAIL-NEW: {node} (a protected test gained a skip/xfail marker)")
    for node in sorted(old_marked - live_marked):
        if ordinary(node):
            expected.append(f"SKIP-XFAIL-ORDINARY-REMOVED: {node} (ordinary marker change)")
    actual = []
    for line in report.decode("utf-8", "replace").splitlines():
        item = line.strip()
        if item.startswith("[gate-manifest] note: "):
            item = item[len("[gate-manifest] note: "):]
        if item.startswith("COLLECTION-") or item.startswith("SKIP-XFAIL-"):
            actual.append(item)
    if sorted(actual) != sorted(expected):
        raise Refuse("P report collection deltas do not match the same-call live collection capture.")


def _unique_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate {label} key {key!r}")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def _validate_collection_capture(raw, *, nonce, prior, candidate, target, verifier_exit):
    collection = _unique_json(raw, "collection")
    node_ids, marked = collection.get("node_ids"), collection.get("skip_xfail_marked")
    if (set(collection) != {"nonce", "prior_anchor", "candidate", "target_repo", "call_count",
                           "exit", "verifier_exit", "node_ids", "skip_xfail_marked"}
            or collection.get("nonce") != nonce or collection.get("prior_anchor") != prior
            or collection.get("candidate") != candidate or collection.get("target_repo") != str(target)
            or type(collection.get("call_count")) is not int or collection.get("call_count") != 1
            or type(collection.get("exit")) is not int or collection["exit"] != 0
            or type(collection.get("verifier_exit")) is not int
            or collection["verifier_exit"] not in (0, 1)
            or collection["verifier_exit"] != verifier_exit
            or not isinstance(node_ids, list) or not node_ids
            or any(not isinstance(n, str) for n in node_ids)
            or node_ids != sorted(set(node_ids)) or not isinstance(marked, list)
            or any(not isinstance(n, str) for n in marked)
            or marked != sorted(set(marked)) or not set(marked).issubset(node_ids)):
        raise Refuse("P collection capture is stale, malformed, duplicate, incomplete, or not from one verifier call.")
    return collection


def _verifier_run(evidence_dir, expected_fingerprint, dispositions=None, *, confirm_key_away=False):
    evidence = _plain_absolute_path(evidence_dir)
    packet_path = evidence / VERIFIER_PACKET
    if packet_path.is_symlink() or not packet_path.is_file():
        raise Refuse("prior verifier evidence packet is missing or a symlink.")
    packet = _unique_json(packet_path.read_bytes(), "verifier evidence")
    if packet.get("schema") != "cairn-prior-verifier-evidence/v1":
        raise Refuse("prior verifier evidence packet has an unknown schema.")
    repo, prior, candidate = Path(packet["trusted_repo"]), packet["prior_anchor"], packet["candidate"]
    if packet.get("expected_fingerprint") != expected_fingerprint:
        raise Refuse("the expected signer fingerprint changed; prepare and review a fresh packet.")
    if sha(Path(__file__).read_bytes()) != packet.get("preparer_sha256"):
        raise Refuse("the preparation script changed since the evidence packet was made.")
    prior_now = git_text(repo, "rev-parse", "--verify", prior + "^{commit}")
    candidate_now = git_text(repo, "rev-parse", "--verify", candidate + "^{commit}")
    if (prior_now != prior or candidate_now != candidate
            or git_text(repo, "rev-parse", "--verify", packet["trusted_ref"] + "^{commit}")
            != packet["trusted_ref"]):
        raise Refuse("P, C, or trusted ref moved; prepare and review fresh evidence.")
    roster_path = _plain_absolute_path(evidence / "prior" / "allowed_signers")
    if roster_path.read_bytes() != git(repo, "cat-file", "blob", f"{prior}:{ROSTER_REL}"):
        raise Refuse("prior signer roster differs from immutable P.")
    good, state, signer = verify_checkpoint(repo, prior, roster_path, expected_fingerprint)
    if not good or signer != packet["signer_fingerprint"]:
        raise Refuse(f"P signature/fingerprint no longer verifies ({state}, {signer!r}).")
    manifest_raw = git(repo, "cat-file", "blob", f"{prior}:{VERIFIER_MANIFEST_REL}")
    frozen = json.loads(manifest_raw).get("frozen_files", {})
    dependencies = packet["prior_dependencies"]
    if set(dependencies) != set(VERIFIER_SCANNER_PATHS) | {VERIFIER_MANIFEST_REL}:
        raise Refuse("prior verifier dependency set differs from the complete required set.")
    for rel in VERIFIER_SCANNER_PATHS:
        entry = frozen.get(rel)
        pinned = entry if isinstance(entry, str) else entry.get("sha256") if isinstance(entry, dict) else None
        if not pinned or dependencies[rel] != pinned:
            raise Refuse(f"prior verifier dependency is not pinned by P at {d(rel)}.")
    if (dependencies[VERIFIER_MANIFEST_REL] != sha(manifest_raw)
            or packet.get("manifest_sha256") != sha(manifest_raw)
            or packet.get("verifier_sha256") != dependencies[VERIFIER_REL]):
        raise Refuse("prior verifier or manifest digest differs from immutable P.")
    for rel, expected in dependencies.items():
        raw = git(repo, "cat-file", "blob", f"{prior}:{rel}", check=False)
        path = _plain_absolute_path(evidence / "prior" / ("gate_manifest.json" if rel == VERIFIER_MANIFEST_REL else rel))
        if raw is None or sha(raw) != expected or path.is_symlink() or path.read_bytes() != raw:
            raise Refuse(f"prior verifier evidence changed at {d(rel)}; prepare again.")
    observer = _plain_absolute_path(packet["observer"])
    if observer != evidence / "verifier-observer.py":
        raise Refuse("observer is not the prepared evidence directory's observer.")
    if (packet.get("observer_sha256") != sha(OBSERVER_SOURCE.encode())
            or observer.is_symlink() or not observer.is_file()
            or sha(observer.read_bytes()) != packet["observer_sha256"]):
        raise Refuse("the collection observer differs from the reviewed preparation code.")
    target = _plain_absolute_path(packet["target"])
    if target != evidence / "candidate":
        raise Refuse("candidate target is not the prepared evidence directory's candidate.")
    _assert_candidate_bytes(repo, candidate, target)
    manifest_obj = json.loads((evidence / "prior" / "gate_manifest.json").read_bytes())
    pinned_version = manifest_obj.get("interpreter", {}).get("version_info", [])
    if list(sys.version_info[:2]) != list(pinned_version[:2]):
        raise Refuse("the canonical interpreter minor does not match P's signed manifest.")
    python = packet["python"]
    current_python = os.path.realpath(sys.executable)
    if (not isinstance(python, str) or python != current_python
            or packet.get("python_sha256") != sha(Path(current_python).read_bytes())):
        raise Refuse("the reviewed Python executable differs from this running interpreter.")
    if not confirm_key_away:
        raise Refuse("explicitly confirm the signing key is away before full collection.")
    say("The following full collection executes candidate code. Confirm the signing key is away and type YES.")
    if input("Signing key away? [YES]: ").strip() != "YES":
        raise Refuse("operator did not confirm key absence; verifier was not run.")
    verifier = evidence / "prior" / VERIFIER_REL
    manifest = evidence / "prior" / "gate_manifest.json"
    env = {"HOME": "/nonexistent", "PATH": "/usr/bin:/bin", "LC_ALL": "C",
           "PYTHONDONTWRITEBYTECODE": "1"}
    nonce = secrets.token_hex(16)
    capture = evidence / f"verifier-collection-{nonce}.json"
    if capture.exists() or capture.is_symlink():
        raise Refuse("fresh collection capture path already exists; choose a new evidence folder.")
    verifier_args = ["verify", "--target-repo", str(target), "--manifest", str(manifest),
                     "--anchor-ref", prior, "--require-anchor", "--trusted-repo", str(repo),
                     "--trusted-ref", prior]
    argv = [python, "-I", "-E", "-s", "-B", str(observer), str(capture), nonce, prior,
            candidate, str(verifier), *verifier_args]
    say("Running authenticated P verifier with full collection.")
    say("verifier argv " + json.dumps(argv))
    result = subprocess.run(argv, cwd="/", env=env, capture_output=True, text=True, check=False)
    report = (result.stdout + result.stderr).encode("utf-8", "replace")
    report_sha = sha(report)
    if capture.is_symlink() or not capture.is_file():
        raise Refuse("P verifier did not produce the full live collection record.")
    capture_raw = capture.read_bytes()
    collection = _validate_collection_capture(capture_raw, nonce=nonce, prior=prior,
                                              candidate=candidate, target=target,
                                              verifier_exit=result.returncode)
    if result.returncode != collection["verifier_exit"]:
        raise Refuse("the prior verifier process and captured collection have inconsistent exit results.")
    if ((result.returncode == 1 and b"[gate-manifest] HOLD" not in report)
            or (result.returncode == 0 and b"[gate-manifest] OK" not in report)):
        raise Refuse("the prior verifier exited without a matching complete report disposition.")
    _verify_collection_report(manifest_obj, collection, report)
    good, state, signer = verify_checkpoint(repo, prior, roster_path, expected_fingerprint)
    if not good or signer != packet["signer_fingerprint"]:
        raise Refuse(f"P signature/fingerprint changed during candidate collection ({state}, {signer!r}).")
    for rel, expected in packet["prior_dependencies"].items():
        raw = git(repo, "cat-file", "blob", f"{prior}:{rel}", check=False)
        path = _plain_absolute_path(evidence / "prior" / ("gate_manifest.json" if rel == VERIFIER_MANIFEST_REL else rel))
        if raw is None or sha(raw) != expected or path.is_symlink() or path.read_bytes() != raw:
            raise Refuse(f"prior verifier evidence changed during collection at {d(rel)}.")
    if sha(Path(current_python).read_bytes()) != packet["python_sha256"]:
        raise Refuse("the reviewed Python executable changed during collection.")
    if observer.is_symlink() or sha(observer.read_bytes()) != packet["observer_sha256"]:
        raise Refuse("collection observer changed during candidate execution.")
    (evidence / "verifier-report.txt").write_bytes(report)
    collection_semantic = dump({"node_ids": collection["node_ids"],
                                "skip_xfail_marked": collection["skip_xfail_marked"],
                                "exit": collection["exit"]})
    _assert_candidate_bytes(repo, candidate, target)
    holds = [ln.strip() for ln in report.decode("utf-8", "replace").splitlines()
             if ln.startswith("  ") and not ln.lstrip().startswith("[gate-manifest]")]
    notes = [ln.strip() for ln in report.decode("utf-8", "replace").splitlines()
             if ln.strip().startswith("[gate-manifest] note:")]
    bound_argv = [python, "-I", "-E", "-s", "-B", str(observer), "<fresh-capture>",
                  "<fresh-nonce>", prior, candidate, str(verifier), *verifier_args]
    binding = {"schema": "cairn-verifier-report-binding/v1", "prior_anchor": prior,
               "candidate": candidate, "verifier_sha256": packet["verifier_sha256"],
               "manifest_sha256": packet["manifest_sha256"], "report_sha256": report_sha,
               "preparer_sha256": packet["preparer_sha256"],
               "python_sha256": packet["python_sha256"],
               "collection_baseline_sha256": sha(dump(manifest_obj.get("collection", {}))),
               "collection_result_sha256": sha(collection_semantic),
               "collection_nonce": nonce, "collection_path": str(capture),
               "observer_sha256": packet["observer_sha256"],
               "collection_node_count": len(collection["node_ids"]),
               "collection_marked_count": len(collection["skip_xfail_marked"]),
               "argv": bound_argv, "environment": env,
               "exit": result.returncode, "holds": holds, "notes": notes}
    binding_path = evidence / "verifier-report-binding.json"
    binding_path.write_bytes(dump(binding))
    say(f"report    {evidence / 'verifier-report.txt'} sha256 {report_sha}")
    say(f"collection {capture} sha256 {binding['collection_result_sha256']} "
        f"({binding['collection_node_count']} nodes, {binding['collection_marked_count']} marked)")
    say(f"binding   {binding_path}")
    say(f"HOLDs ({len(holds)}):")
    for line in holds:
        say("  " + line)
    say(f"ordinary notes ({len(notes)}):")
    for line in notes:
        say("  " + line)
    if result.returncode != 0:
        if not holds:
            raise Refuse("prior verifier returned nonzero without a complete displayed HOLD list; no disposition can cover it.")
        disposition_path = Path(dispositions) if dispositions else evidence / f"verifier-dispositions-{nonce}.json"
        if dispositions:
            _check_dispositions(disposition_path, binding)
            say("Recorded dispositions match every exact HOLD and this report. The underlying verifier remains HOLD; this consistency check does not authorize signing or continuation.")
            return 1
        else:
            _write_disposition_template(disposition_path, binding)
            say(f"No signing authorization: verifier returned {result.returncode}. Review and disposition every displayed HOLD: {disposition_path}")
        return 1
    if dispositions and binding["holds"]:
        _check_dispositions(Path(dispositions), binding)
        say("All report items have explicit recorded human dispositions bound to this P/C/report. This does not authorize signing or waive any HOLD.")
    return 0


def _write_disposition_template(path, binding):
    obj = {**binding, "items": [{"item": h, "disposition": "", "reason": ""}
                                 for h in binding["holds"]]}
    with open(path, "xb") as stream:
        stream.write(dump(obj))


def _check_dispositions(path, binding):
    if path.is_symlink() or not path.is_file():
        raise Refuse("disposition record is missing or a symlink.")
    obj = _unique_json(path.read_bytes(), "disposition")
    for key in ("schema", "prior_anchor", "candidate", "preparer_sha256", "python_sha256", "verifier_sha256", "manifest_sha256", "observer_sha256", "report_sha256", "collection_baseline_sha256", "collection_result_sha256", "collection_node_count", "collection_marked_count", "argv", "environment", "exit", "holds", "notes"):
        if obj.get(key) != binding.get(key):
            raise Refuse(f"disposition evidence is stale or differs at {key}; fresh review is required.")
    items = obj.get("items")
    if not isinstance(items, list) or [i.get("item") for i in items] != binding["holds"]:
        raise Refuse("dispositions do not cover the exact currently displayed HOLD set.")
    if any(i.get("disposition") not in ("proceed", "stop", "defer")
           or not isinstance(i.get("reason"), str) or not i["reason"].strip() for i in items):
        raise Refuse("every HOLD needs a proceed, stop, or defer disposition and a specific human reason.")


def anchor_state(ctx, roster):
    """('G', fp) good; ('N', ...) unsigned; anything else is a signature that fails."""
    ok, status, key = verify_checkpoint(ctx["repo"], ctx["anchor"], roster, None)
    return status, key


def last_signed(ctx, roster):
    rows = git(ctx["repo"], "-c", "gpg.format=ssh", "-c", f"gpg.ssh.allowedSignersFile={roster}",
               "-c", f"gpg.ssh.program={KEYGEN}", "-c", f"gpg.program={os.devnull}",
               "-c", f"gpg.openpgp.program={os.devnull}", "-c", f"gpg.x509.program={os.devnull}",
               "log", "--first-parent", "-n", "2000",
               "--format=%H%x00%G?", ctx["anchor"]).decode().splitlines()
    for n, row in enumerate(rows):
        if row.endswith("\0G"):
            return row.split("\0")[0], n
    return None, len(rows)


def check_stop_records(ctx, cdir, first_run):
    """Every commit since the anchor that changes an output path must be the commit
    a stop record in *cdir* describes: one parent (the recorded HEAD), exactly the
    recorded paths at the recorded blobs.  Compared from raw diff-tree output."""
    repo, anchor, head = ctx["repo"], ctx["anchor"], ctx["head"]
    recs = [json.loads(read_safe(f, own=True)) for f in sorted(Path(cdir).glob(STOP_PREFIX + "*.json"))]
    span = f"{anchor}..{head}"
    # Path-limited listings print rewritten parents, so ask for each commit's real ones.
    listed = set(git_text(repo, "rev-list", "--full-history", span, "--", *OUTPUTS).split())
    listed |= set(git_text(repo, "rev-list", "--merges", span).split())
    for name in sorted(listed):
        commit, *parents = git_text(repo, "rev-list", "--parents", "-n", "1", name).split()
        if not any(blob_at(repo, commit, o) != blob_at(repo, p, o) for p in parents for o in OUTPUTS):
            continue
        changed = {}
        if len(parents) == 1:
            parts = git(repo, "diff-tree", "-r", "-z", "--no-renames", "--no-commit-id", "--raw", commit).split(b"\0")
            changed = {parts[i + 1].decode("utf-8", "surrogateescape"): parts[i].split()[3].decode()
                       for i in range(0, len(parts) - 1, 2)}
        if len(parents) == 1 and any(r["head"] == parents[0] and r["paths"] == changed for r in recs):
            say(f"  commit {commit[:12]} matches a stop record: it changes exactly the paths and bytes written")
            continue
        msg = (f"commit {commit[:12]} changes {', '.join(OUTPUTS)} but matches no stop record in "
               f"{d(str(cdir))}: it is a merge, has another parent, adds a path, or holds other bytes "
               f"than the ones shown to you. To undo it: git revert {commit}")
        if not first_run:
            raise Refuse(msg)
        say("  shown, not refused (first run): " + msg)


def check_first_run(ctx, reviewed):
    repo = ctx["repo"]
    if ctx["repin_state"] == "anchored":
        raise Refuse("--first-run is for a repin the anchor does not yet pin, and this one is anchored. "
                     "Run without --first-run.")
    if not reviewed:
        raise Refuse("--first-run needs --reviewed-commit <id>: the last commit that edited repin or "
                     "its tests and that the code reviewer read.")
    rid = git(repo, "rev-parse", "--verify", reviewed + "^{commit}", check=False)
    if rid is None or git(repo, "merge-base", "--is-ancestor", rid.decode().strip(), ctx["head"],
                          check=False) is None:
        raise Refuse(f"{d(reviewed)} is not a commit that is an ancestor of HEAD.")
    for path in (REPIN_REL, *REPIN_TESTS):
        was = blob_at(repo, rid.decode().strip(), path)
        if was is None or was != blob_at(repo, ctx["head"], path):
            raise Refuse(f"{path} at HEAD is not the file the reviewed commit has. It was edited "
                         f"after review; a new review must name a newer commit.")
    txn = build_transaction(ctx)
    if txn is not None and set(txn["outputs"]) != {LOCKFILE_REL}:
        raise Refuse("a pin is owed (the AST baseline). The first run never carries one, because "
                     "repin's own unpinned bytes would decide it. Pin it by hand under "
                     "bootstrap/AST_BASELINE_RUNBOOK.md first.")
    if txn is None:
        say(NOTHING_OWED)
    else:
        say("\nA lockfile correction is owed. The first run does not apply it: the ordinary ceremony "
            "after this one does.")
        for line in txn["summary"]:
            say(line)


def anchored_template(ctx):
    """The launcher template as the anchor holds it, and the closure its fixed list names."""
    raw = git(ctx["repo"], "cat-file", "blob", f"{ctx['anchor']}:{TEMPLATE_REL}", check=False)
    if raw is None or raw.count(SLOT.encode()) != 1:
        raise Refuse(f"the anchor has no {TEMPLATE_REL} with exactly one {SLOT} slot.")
    try:
        members = ctx["rc"].closure_members(ctx["repo"], ctx["anchor"])
    except SystemExit:
        raise Refuse(f"the closure list in the anchor's {TEMPLATE_REL} could not be read.")
    if sorted(members) != sorted(ctx["closure"]):
        raise Refuse("the launcher template's closure list differs from the checker's declared closure, "
                     "so the closure shown here cannot be trusted. Nothing was run.")
    return raw, members


def write_new(path, raw):
    """Create *path* and write *raw*; refuse an existing file or a link."""
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    except OSError as exc:
        raise Refuse(f"{d(str(path))} cannot be created ({exc.strerror}). Move it aside, then run again.")
    with os.fdopen(fd, "wb") as fh:
        fh.write(raw)


def build_packet(ctx, cdir, *, transition=False, baseline=False):
    """`packet`: write the packet over HEAD's authority files and the launcher (the anchor's
    template with the packet's digest in its one slot).  Ordinary ceremonies only: a changed
    authority file means the packet and launcher are built by hand, so nothing is written.

    Baseline mode uses the same exclusive packet writer for the independently
    checked manifest/package pair; it is selected by the explicit baseline
    preparation command and never enters the ordinary ceremony path.
    """
    if baseline:
        output = _plain_absolute_path(cdir)
        if output.exists() or output.is_symlink() or output == ctx["repo"] or ctx["repo"] in output.parents:
            raise Refuse("baseline package destination must be new and outside the checkout.")
        output.mkdir()
        try:
            write_new(output / "gate_manifest.json", ctx["baseline_manifest"])
            write_new(output / "baseline-package.json", dump(ctx["baseline"]))
        except BaseException:
            shutil.rmtree(output, ignore_errors=True)
            raise
        return sha(dump(ctx["baseline"]))
    if ctx["closure_changed"] and not transition:
        raise Refuse("these authority files differ from the anchor: "
                     + ", ".join(d(m) for m in ctx["closure_changed"])
                     + f". That is a transition ceremony; its packet and launcher are built by hand "
                     f"under {RUNBOOK}. Nothing was written.")
    if transition and not ctx["closure_changed"]:
        raise Refuse("the authority closure is unchanged; use the ordinary packet command.")
    check_preconditions(ctx, need_terminal=False)
    cdir = plain_folder(cdir)
    template, members = anchored_template(ctx)
    gone = [m for m in members if not (ctx["ext"] / m).is_file()]
    if gone:
        raise Refuse("HEAD does not track " + ", ".join(d(m) for m in gone) + ". Nothing was written.")
    rows = [f"member {sha((ctx['ext'] / m).read_bytes())} {m}" for m in members]
    packet = "\n".join([f"schema {PACKET_SCHEMA}", "provenance repin packet", f"artifact {ARTIFACT_REL}",
                        f"artifact_sha256 {sha((ctx['ext'] / ARTIFACT_REL).read_bytes())}", *rows]).encode() + b"\n"
    launcher = template.replace(SLOT.encode(), sha(packet).encode())
    paths = cdir / PACKET_NAME, cdir / LAUNCHER_NAME
    if any(os.path.lexists(p) for p in paths):
        raise Refuse(f"{d(str(cdir))} already holds a packet or a launcher. Move them aside, then run "
                     f"again. Nothing was written.")
    write_new(paths[0], packet)
    try:
        write_new(paths[1], launcher)
    except Refuse:
        paths[0].unlink()
        raise
    say(f"\nwrote {d(str(paths[0]))}\n  sha256 {sha(packet)}\nwrote {d(str(paths[1]))}\n  sha256 {sha(launcher)}")
    say(f"HEAD, the commit the reader reads  {ctx['head']}\n"
        f"Give the reader these three values. The record ({RECORD_REL}) names them and is committed on "
        f"this HEAD, changing only that file.")


def prepare_reader_inputs(ctx, cdir, output):
    """Prepare facts for a separate reader; this is not the reader's record."""
    cdir = _plain_absolute_path(cdir)
    output = _plain_absolute_path(output)
    repo = ctx["repo"]
    if output == repo or repo in output.parents:
        raise Refuse("reader inputs must be written outside the checkout.")
    packet = cdir / PACKET_NAME
    launcher = cdir / LAUNCHER_NAME
    packet_raw, launcher_raw = read_safe(packet), read_safe(launcher)
    template, members = anchored_template(ctx)
    if launcher_raw != template.replace(SLOT.encode(), sha(packet_raw).encode()):
        raise Refuse("launcher differs from the prior template and packet.")
    try:
        state = ctx["rc"].compare(repo, ctx["head"], packet)
    except SystemExit:
        raise Refuse("candidate and packet could not be compared.")
    if not ctx["rc"].check_packet_pair(state, packet, launcher):
        raise Refuse("candidate, packet and launcher do not agree.")
    lines = ["# Reader inputs -- verify independently before writing a record",
             f"read-commit {ctx['head']}", f"prior-anchor {ctx['anchor']}",
             f"packet-sha256 {sha(packet_raw)}", f"launcher-sha256 {sha(launcher_raw)}"]
    lines.extend(f"member {sha((ctx['ext'] / m).read_bytes())} {m}" for m in members)
    transaction = cdir / TXN_NAME
    if transaction.exists() or transaction.is_symlink():
        txn_raw = read_safe(transaction, own=True)
        txn = json.loads(txn_raw)
        expected = build_transaction(ctx, reviewed_deletions=txn.get("reviewed_deletions", ()))
        if expected is None or encode_txn(expected) != txn_raw:
            raise Refuse("prepared transaction does not match this read commit.")
        lines.append(f"ast-transaction-sha256 {sha(txn_raw)}")
    raw = ("\n".join(lines) + "\n").encode()
    write_new(output, raw)
    say(f"wrote reader inputs {d(str(output))} sha256 {sha(raw)}")
    say("These are preparation data, not an independent review or authorization.")


def record_values(text):
    """The record's digest lines as data: the commit read, the packet, the launcher and each
    member.  A line repeated is a record that disagrees with itself."""
    one, members = {}, {}
    for line in text.splitlines():
        m = re.fullmatch(r"(read-commit) ([0-9a-f]{40,64})|(packet-sha256|launcher-sha256) ([0-9a-f]{64})", line)
        if m:
            key, val = (m[1], m[2]) if m[1] else (m[3], m[4])
            if key in one:
                raise Refuse(f"{RECORD_REL} states {key} twice.")
            one[key] = val
            continue
        m = re.fullmatch(r"member ([0-9a-f]{64}) (\S+)", line)
        if m:
            if m[2] in members:
                raise Refuse(f"{RECORD_REL} names {d(m[2])} twice.")
            members[m[2]] = m[1]
    return one, members


def check_record(ctx, packet_digest, launcher_digest, *, baseline_record=None):
    """The reader's record is the candidate's tip: committed on the commit the reader read,
    changing only itself, and naming this packet, this launcher and these member bytes."""
    if baseline_record is not None:
        path = _plain_absolute_path(baseline_record)
        if path.is_symlink() or not path.is_file():
            raise Refuse("independent baseline reader record is missing or a symlink.")
        record = _unique_json(path.read_bytes(), "baseline reader record")
        package = ctx["baseline"]
        expected = {"schema": "cairn-baseline-reader/v1", "candidate": package["candidate"],
                    "roster_sha256": package["roster_sha256"],
                    "manifest_sha256": package["manifest_sha256"],
                    "collection_sha256": package["collection_sha256"],
                    "interpreter": package["interpreter"], "tool_hashes": package["tool_hashes"]}
        if (set(record) != set(expected) | {"reviewer", "reviewed"}
                or any(record.get(key) != value for key, value in expected.items())):
            raise Refuse("independent baseline reader record is stale or mismatched.")
        if (record.get("reviewed") is not True or not isinstance(record.get("reviewer"), str)
                or not record["reviewer"].strip()
                or package["reader_record_sha256"] != sha(path.read_bytes())):
            raise Refuse("independent baseline reader record lacks review attribution or digest binding.")
        return
    repo, head, ext = ctx["repo"], ctx["head"], ctx["ext"]
    if not (ext / RECORD_REL).is_file():
        raise Refuse(f"{RECORD_REL} is not committed at HEAD. The reader commits it on the commit "
                     f"they read, before the ceremony. Nothing was run.")
    one, members = record_values((ext / RECORD_REL).read_text("utf-8", "replace"))
    for key in ("read-commit", "packet-sha256", "launcher-sha256"):
        if key not in one:
            raise Refuse(f"{RECORD_REL} has no {key} line.")
    parents = git_text(repo, "rev-list", "--parents", "-n", "1", head).split()[1:]
    if parents != [one["read-commit"]]:
        raise Refuse(f"HEAD's parent is {', '.join(parents) or 'nothing'}, but {RECORD_REL} says the reader "
                     f"read {one['read-commit']}. The record must be the one commit on top of what was read.")
    changed = git(repo, "diff-tree", "-r", "-z", "--no-commit-id", "--name-only", "--no-renames", head)
    names = [n.decode("utf-8", "surrogateescape") for n in changed.split(b"\0") if n]
    if names != [RECORD_REL]:
        raise Refuse("the record commit changes more than the record: "
                     + ", ".join(d(n) for n in names) + f". It may change only {RECORD_REL}.")
    want = {m: sha((ext / m).read_bytes()) for m in ctx["closure"]}
    for what, got, said in (("packet", packet_digest, one["packet-sha256"]),
                            ("launcher", launcher_digest, one["launcher-sha256"]),
                            ("authority files", want, members)):
        if got != said:
            raise Refuse(f"the {what} differ from the ones {RECORD_REL} names. Do not run this.")


def apply_reviewed_pin(ctx, cdir):
    """Apply only the transaction the independent record bound before writing."""
    check_preconditions(ctx)
    cdir = plain_folder(cdir)
    packet = read_safe(cdir / PACKET_NAME)
    launcher = read_safe(cdir / LAUNCHER_NAME)
    check_record(ctx, sha(packet), sha(launcher))
    raw = read_safe(cdir / TXN_NAME, own=True)
    record = (ctx["ext"] / RECORD_REL).read_text("utf-8")
    matches = re.findall(r"^ast-transaction-sha256 ([0-9a-f]{64})$", record, re.M)
    if matches != [sha(raw)]:
        raise Refuse("the reader record does not bind this exact AST transaction.")
    txn = json.loads(raw)
    parents = git_text(ctx["repo"], "rev-list", "--parents", "-n", "1", ctx["head"]).split()[1:]
    if parents != [txn.get("head")]:
        raise Refuse("the reader record must be the sole child of the transaction's read commit.")
    prior_ctx = dict(ctx, head=txn["head"])
    expected = build_transaction(prior_ctx, reviewed_deletions=txn.get("reviewed_deletions", ()))
    if expected is None or encode_txn(expected) != raw:
        raise Refuse("the transaction no longer matches the independently reviewed commit.")
    return apply_pin(ctx, cdir, raw, reviewed_head=txn["head"])


def write_record(cdir, lines):
    raw = ("\n".join(lines) + "\n").encode()
    fd, tmp = tempfile.mkstemp(dir=cdir, prefix=".record-")
    with os.fdopen(fd, "wb") as fh:
        fh.write(raw)
    os.replace(tmp, Path(cdir) / "ceremony-record.txt")
    return Path(cdir) / "ceremony-record.txt", sha(raw)


def run_ceremony(ctx, args, launchctl, rec):
    rc, repo, tmp = ctx["rc"], ctx["repo"], ctx["tmp"]
    cdir, values = Path(args.ceremony_dir), Path(args.values)
    check_preconditions(ctx)
    packet, launcher = cdir / "authorization-packet.txt", cdir / "reanchor-launcher.sh"
    field = {k: rc.values_field(values, k) for k in ("checkout", "signing_key", "package", "home", "python")}
    if None in field.values() or Path(field["checkout"]).resolve() != repo:
        raise Refuse("the values file must name checkout, signing_key, package, home and python, and its "
                     "checkout must be this repository.")
    pub = field["signing_key"]
    private = pub[:-4] if pub.endswith(".pub") else pub
    term = os.environ.get("TERM", "xterm")
    rec.append(f"repin ceremony at HEAD {ctx['head']}, anchor {ctx['anchor']}, python "
               f"{sys.version.split()[0]}, git {GIT} sha256 "
               f"{sha(Path(GIT).read_bytes()) if os.path.isfile(GIT) else 'unreadable'}")
    # 1. the launcher's digest, compared by eye and by this program
    ldigest = sha(read_safe(launcher))
    try:
        pasted = input("\nPaste the launcher digest from the record: ").strip()
    except EOFError:
        pasted = ""
    say(f"  launcher {d(str(launcher))}\n  computed {ldigest}\n  pasted   {d(pasted)}")
    if pasted != ldigest:
        raise Refuse("the launcher's digest is not the one in the record. Do not run it.")
    rec.append(f"launcher digest {ldigest} equals the pasted digest")
    confirm(rec, "Do the two digests match?")

    # The python the values file names, and the values file itself, are files stage 1's candidate
    # tests can rewrite before stage 2 starts them with the key about to be typed. Hashing them
    # before each run catches a change to those two files only; the interpreter's library folder
    # and the other tools stay as writable as before, so this is not containment.
    watched = {"the values file": values, "the python the values file names": Path(field["python"])}
    seen = {name: sha(read_safe(path)) for name, path in watched.items()}
    rec.append("values file digest " + seen["the values file"] + ", python digest "
               + seen["the python the values file names"])

    def launcher_unchanged():
        """The launcher runs twice, minutes and a prompt apart; it, the values file and the python
        are hashed before each run."""
        if sha(read_safe(launcher)) != ldigest:
            raise Refuse("the launcher changed after its digest was compared. Nothing further was run.")
        for name, path in watched.items():
            if sha(read_safe(path)) != seen[name]:
                raise Refuse(f"{name} changed after the ceremony started. Nothing further was run.")
    # 2. packet, launcher, artifact and values
    try:
        state = rc.compare(repo, ctx["head"], packet)
    except SystemExit as exc:
        raise Refuse(f"the closure could not be compared (exit {exc.code}).")
    if sorted(state["members"]) != sorted(ctx["closure"]):
        raise Refuse("the launcher template's closure list differs from the checker's declared closure, "
                     "so the closure shown here cannot be trusted. Nothing was run.")
    if not rc.check_packet_pair(state, packet, launcher):
        raise Refuse("the packet and launcher are not the pair the launcher demands.")
    want = rc.packet_artifact_digest(packet)
    art = (ctx["ext"] / ARTIFACT_REL).read_bytes()
    if sha(art) != want:
        raise Refuse(f"{ARTIFACT_REL} at HEAD is not the artifact the packet authorises. Nothing was run.")
    # A2: the launcher is the anchor's template with the packet's digest in its one slot, byte for
    # byte, so the reviewed text and the run text are one.  Checked before any child is started.
    anchored, _members = anchored_template(ctx)
    if read_safe(launcher) != anchored.replace(SLOT.encode(), sha(read_safe(packet)).encode()):
        raise Refuse("the launcher is not the anchor's launcher template with the packet's digest in "
                     "its one slot. Do not run it. Nothing was run.")
    check_record(ctx, sha(read_safe(packet)), ldigest)
    rec.append(f"record {RECORD_REL} names the read commit, this packet, this launcher and these files")

    def reading(command):
        """validate, show-report and hash-package run through the launcher, which verifies the
        artifact and reads the values file before the artifact starts; the launcher is hashed first."""
        launcher_unchanged()
        env = {"PATH": CHILD_PATH, "HOME": field["home"], "LC_ALL": "C"}
        return child(rec, [SH, str(launcher), str(packet), str(values), ctx["head"], "--" + command], env=env)
    r = reading("validate")
    if r.returncode:
        relay(r.stdout + r.stderr)
        raise Refuse("the launcher's validate refused the values file. No report was shown.")
    # 3. roster and anchor. During a reviewed authority transition the old
    # anchor must be checked with its own roster, while the candidate roster
    # remains the authority for the signature this ceremony will create.
    roster = tmp / "roster"
    roster.write_bytes((ctx["ext"] / ROSTER_REL).read_bytes())
    fingerprint = key_fingerprint(rec, pub)
    rec.append(f"signing key fingerprint {fingerprint}")
    kt, kd = Path(pub).read_text().split()[:2]
    if not any(kt in t and kd in t and t.index(kd) == t.index(kt) + 1
               for t in (ln.split() for ln in roster.read_text().splitlines())):
        raise Refuse(f"the signing key {fingerprint} is not in the packet-pinned roster.")
    anchor_roster = roster
    if args.transition:
        if not ctx["prior_authority"] or not re.fullmatch(
                r"SHA256:[A-Za-z0-9+/]{43}", args.expected_fingerprint or ""):
            raise Refuse("a transition ceremony needs prior-authority boot and an independently trusted fingerprint.")
        anchor_roster = ctx["tmp"] / "authority-roster"
        anchor_roster.write_bytes((ctx["tmp"] / "authority" / ROSTER_REL).read_bytes())
    status, signer = anchor_state(ctx, anchor_roster)
    if args.transition and (status != "G" or signer != args.expected_fingerprint):
        raise Refuse(f"the prior anchor must verify with the independently trusted fingerprint "
                     f"({status}, {signer!r}, expected {args.expected_fingerprint}).")
    if status == "N" and args.first_run:
        known, n = last_signed(ctx, roster)
        say(f"  the comparison base {ctx['anchor']} is unsigned; the last signed anchor is "
            f"{known or 'not found'}, {n} commits earlier; what this ceremony blesses since then "
            f"rests on the launcher digest you compared.")
    elif status != "G":
        raise Refuse(f"the anchor {ctx['anchor']} has signature state {d(status)}, not a good signature "
                     f"by a roster key. " + ("An unsigned anchor needs --first-run." if status == "N"
                                             else "--first-run does not waive a signature that fails."))
    # 4. the reading order's last findings
    if ctx["closure_changed"] and not args.transition:
        raise Refuse("authority files differ from the anchor: " + ", ".join(d(m) for m in ctx["closure_changed"])
                     + f". That is a transition ceremony. Run it by hand under {RUNBOOK}.")
    if args.transition and not ctx["closure_changed"]:
        raise Refuse("--transition requires changed authority files; use the ordinary ceremony.")
    if args.first_run:
        check_first_run(ctx, args.reviewed_commit)
    elif args.reviewed_commit or ctx["repin_state"] != "anchored":
        raise Refuse(f"{REPIN_REL} is {ctx['repin_state']}; its bytes are not the anchor's. Only the "
                     f"first run may continue, with --first-run --reviewed-commit <id>.")
    check_stop_records(ctx, cdir, args.first_run)
    key_checks(rec, pub, private, fingerprint, launchctl, "before stage 1")
    # 5. an owed pin is written, then this stops (a first run shows a lockfile correction and leaves it)
    if not args.first_run and not args.transition and build_transaction(ctx) is not None:
        raise Refuse("an AST or lockfile transaction is owed. Prepare it at the read commit, "
                     "have the reader record its digest, then run apply-reviewed-pin. "
                     "No files were written.")
    # Read the prior scanner before stage 1 can run candidate code. Keep the
    # result in this process until the report is available for comparison.
    prior_scan = None
    if not args.first_run:
        scan = reading("scan-digest")
        scan_lines = scan.stdout.splitlines()
        if scan.returncode or not scan_lines or not re.fullmatch(r"[0-9a-f]{64}", scan_lines[-1]):
            raise Refuse("the prior scanner failed; nothing was signed.")
        prior_scan = scan_lines[-1]
    # 6. stage 1: candidate code runs, in a new session with no terminal and a short environment
    if Path(field["package"]).exists():
        raise Refuse(f"{d(field['package'])} already exists; stage 1 must not overwrite it. Move it aside.")
    env = {"PATH": CHILD_PATH, "HOME": field["home"], "LC_ALL": "C"}
    launcher_unchanged()
    r = child(rec, [SH, str(launcher), str(packet), str(values), ctx["head"]], env=env,
              start_new_session=True)
    relay(r.stdout + r.stderr)
    if r.returncode or not Path(field["package"]).is_file():
        raise Refuse(f"stage 1 failed (exit {r.returncode}). Nothing was signed and no ref moved.")
    # 7. Summary 2
    package_file = Path(field["package"])
    own = sha(read_safe(package_file))
    hashed = reading("hash-package")
    theirs = [t for t in hashed.stdout.split() if len(t) == 64 and t.isalnum()]
    if hashed.returncode or theirs[:1] != [own]:
        raise Refuse("the launcher's hash of the package and this program's disagree.")
    report = reading("show-report")
    if report.returncode:
        raise Refuse("the launcher could not show the authorization report. Nothing was signed.")
    # E7 uses the authenticated anchor scanner, independently of the candidate
    # report. Compare the exact digest displayed to the operator before approval.
    if not args.first_run:
        report_digests = re.findall(r"(?m)^\s*scan digest\s+([0-9a-f]{64})\s*$", report.stdout)
        if report_digests != [prior_scan]:
            raise Refuse("the prior scanner and authorization report disagree. Nothing was signed.")
        rec.append(f"prior scanner and report scan digest agree: {prior_scan}")
    say("\nSummary 2: what you are about to sign")
    relay(report.stdout)
    manifest_status(ctx)
    say(f"authority files changed since the anchor: {len(ctx['closure_changed'])} of {len(ctx['closure'])}\n"
        f"anchor signature: {'good, by a roster key' if status == 'G' else 'unsigned (first run)'}\n"
        f"signing key fingerprint: {fingerprint}\npackage digest: {own}")
    rec.append(f"package digest {own}")
    confirm(rec, "Does Summary 2 describe what you intend to sign?")
    if sha(read_safe(package_file)) != own:
        raise Refuse("the package was rewritten after you read the report. Nothing was signed.")
    # 8-9. (signing path) key checks again, then stage 2 with the terminal attached and a short environment
    key_checks(rec, pub, private, fingerprint, launchctl, "before stage 2")
    note = "This key must never be loaded into an agent: the signer asks for its passphrase itself."
    say(f"\nYou will be asked for the key's passphrase once, now. If you are asked at any other point, "
        f"type nothing and stop.\n{note}\nasked once, now")
    env = {"HOME": field["home"], "PATH": CHILD_PATH, "TERM": term, "LANG": "C"}
    argv = [SH, str(launcher), str(packet), str(values), ctx["head"], "--stage2", own]
    launcher_unchanged()
    rec.append(f"ran {' '.join(argv)}")
    proc = subprocess.Popen(argv, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    for raw_line in proc.stdout:
        line = raw_line.decode("utf-8", "replace").rstrip("\n")
        say(d(line))
    rec.append(f"stage 2 exit {proc.wait()}")
    if proc.returncode:
        say(note)
        raise Refuse(f"stage 2 failed (exit {proc.returncode}). Nothing was pushed.")
    # 10-11. (end of signing path) verify against the packet-pinned roster, then end
    new = git_text(repo, "rev-parse", "--verify", ANCHOR_REF + "^{commit}")
    if new == ctx["anchor"]:
        raise Refuse(f"stage 2 exited cleanly but the anchor did not move from {new}. Nothing was "
                     f"signed that this tool can see. Do not push.")
    if git(repo, "merge-base", "--is-ancestor", ctx["anchor"], new, check=False) is None:
        raise Refuse(f"stage 2 left the anchor at {new}, which does not descend from the old anchor "
                     f"{ctx['anchor']}: a checkpoint that is not a move forward. Do not push.")
    good, status, key = verify_checkpoint(repo, new, roster, fingerprint)
    if not good:
        raise Refuse(f"the new anchor {new} does not carry a good signature by {fingerprint} "
                     f"(state {d(status)}, key {d(key)}). Do not push.")
    branch = git_text(repo, "symbolic-ref", "HEAD")
    tip = git_text(repo, "rev-parse", "HEAD")
    rec.append(f"verified: new anchor {new}, good signature by {fingerprint}, branch {branch} at {tip}")
    return new, tip


def finish(ctx, path, digest, done, rec):
    say(f"\nrecord  {d(str(path))}\nrecord digest  {digest}")
    if done:
        new, tip = done
        branch = git_text(ctx["repo"], "symbolic-ref", "HEAD")
        unasked = [ln for ln in rec if "could not be asked" in ln]
        claim = ("The key was not in either agent when asked, before stage 1 and before stage 2." if not unasked
                 else f"{len(unasked)} agent check(s) could not be asked, so the key's absence from those "
                      f"agents is not shown; the record lists them.")
        say(f"Done: the new anchor is {new} and the new {branch} is {tip}; the anchor carries a good "
            f"signature by the roster key.\n{claim}\n"
            f"Publishing is yours; this tool never pushes:\n  git -C {d(str(ctx['repo']))} push --atomic "
            f"origin {branch}:{branch} {ANCHOR_REF}:{ANCHOR_REF}")


def prepare_values(repo, output, signing_key, home, ceremony_dir):
    """Write a fresh, reviewable values file with no authority or secret."""
    repo = _plain_absolute_path(repo)
    output = _plain_absolute_path(output)
    signing_key = _plain_absolute_path(signing_key)
    home = _plain_absolute_path(home)
    cdir = _plain_absolute_path(ceremony_dir)
    if not signing_key.is_file() or not home.is_dir() or not cdir.is_dir():
        raise Refuse("the public key, home and ceremony directory must exist.")
    if repo == cdir or repo in cdir.parents or repo == output or repo in output.parents:
        raise Refuse("the values file and ceremony directory must be outside the checkout.")
    package = cdir / ("authorization-package-" + secrets.token_hex(16) + ".json")
    values = {"schema": "cairn-ceremony-values/v1", "checkout": str(repo),
              "signing_key": str(signing_key), "package": str(package), "home": str(home)}
    for tool in ("env", "git", "python", "mktemp", "mkdir", "shasum", "sort", "cat"):
        located = sys.executable if tool == "python" else shutil.which(tool)
        if not located:
            raise Refuse(f"cannot locate executable {tool}.")
        resolved = Path(os.path.realpath(located))
        if not resolved.is_file() or not os.access(resolved, os.X_OK):
            raise Refuse(f"{tool} is not an executable regular file.")
        values[tool] = str(resolved)
    if any(any(ord(c) < 32 or ord(c) == 127 for c in value) or value.rstrip() != value
           or len((key + " " + value).encode()) > 4096 for key, value in values.items()):
        raise Refuse("a value contains a control character, trailing space or overlong line.")
    raw = "".join(f"{key} {value}\n" for key, value in values.items()).encode()
    write_new(output, raw)
    say(f"wrote values {d(str(output))} sha256 {sha(raw)}")
    say(f"fresh package path {d(str(package))}")
    say("The reader checks every path and digest; the launcher validates the file before use.")


def main(argv=None, *, launchctl=launchctl_socket):
    ap = argparse.ArgumentParser(prog="repin", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    st = sub.add_parser("status", help="show what the pins owe; writes nothing")
    st.add_argument("--dropped-from", metavar="FILE", help="the saved text of a "
                    "`_gate_manifest.py verify` run, to sort its dropped test nodes")
    pk = sub.add_parser("package", help="compute the AST pin's transaction and print its "
                        "digest; writes only into --ceremony-dir")
    pk.add_argument("--ceremony-dir", metavar="DIR", help="a folder to keep the transaction in")
    pk.add_argument("--delete-symbol", action="append", default=[], metavar="KEY",
                    help="exact missing baseline symbol for independent review; repeat for each")
    pt = sub.add_parser("packet", help="write the packet and the launcher for an ordinary ceremony "
                        "into --ceremony-dir; refuses a ceremony that changes an authority file")
    pt.add_argument("--ceremony-dir", required=True, metavar="DIR", help="a folder that holds neither yet")
    vp = sub.add_parser("prepare-values", help="write fresh reviewable ceremony values")
    vp.add_argument("--output", required=True, metavar="FILE")
    vp.add_argument("--signing-key", required=True, metavar="PUBLIC-KEY")
    vp.add_argument("--home", required=True, metavar="DIR")
    vp.add_argument("--ceremony-dir", required=True, metavar="DIR")
    tp = sub.add_parser("transition-packet", help="prepare a packet using authenticated prior authority")
    tp.add_argument("--ceremony-dir", required=True, metavar="DIR")
    tp.add_argument("--expected-fingerprint", required=True, metavar="SHA256:...")
    ri = sub.add_parser("prepare-reader", help="prepare facts for an independent reader")
    ri.add_argument("--ceremony-dir", required=True, metavar="DIR")
    ri.add_argument("--output", required=True, metavar="FILE")
    ri.add_argument("--expected-fingerprint", required=True, metavar="SHA256:...")
    apin = sub.add_parser("apply-reviewed-pin", help="apply a transaction bound by the reader record")
    apin.add_argument("--ceremony-dir", required=True, metavar="DIR")
    cp = sub.add_parser("commit-reviewed-pin", help="commit the approved AST write after a separate yes")
    cp.add_argument("--ceremony-dir", required=True, metavar="DIR")
    ce = sub.add_parser("ceremony", help="the whole re-anchor: checks, an owed AST pin (then stop), "
                        "the launcher's two stages, verification")
    ce.add_argument("--values", required=True, metavar="FILE", help="your values file")
    ce.add_argument("--ceremony-dir", required=True, metavar="DIR", help="holds the packet and "
                    "launcher, and receives the transaction, stop record and record")
    ce.add_argument("--first-run", action="store_true", help="the anchor does not pin this tool yet")
    ce.add_argument("--transition", action="store_true",
                    help="run the script-led ceremony for reviewed changed authority")
    ce.add_argument("--expected-fingerprint", metavar="SHA256:...",
                    help="independently trusted prior signer; required with --transition")
    ce.add_argument("--reviewed-commit", metavar="ID", help="with --first-run: the last commit the "
                    "code reviewer read that edited this tool or its tests")
    pv = sub.add_parser("prepare-verifier", help="prepare signed prior-P verifier and exact candidate evidence")
    pv.add_argument("--trusted-repo", required=True, metavar="REPO")
    pv.add_argument("--prior-anchor", default=ANCHOR_REF, metavar="SHA|REF",
                    help="defaults to the installed gate-anchor ref")
    pv.add_argument("--candidate", default="HEAD", metavar="SHA|REF",
                    help="defaults to the committed HEAD")
    pv.add_argument("--trusted-ref", default=ANCHOR_REF, metavar="REF")
    pv.add_argument("--expected-fingerprint", required=True, metavar="SHA256:...")
    pv.add_argument("--evidence-dir", required=True, metavar="DIR")
    vr = sub.add_parser("verify-candidate", help="run P's full verifier against prepared C and bind dispositions")
    vr.add_argument("--evidence-dir", required=True, metavar="DIR")
    vr.add_argument("--expected-fingerprint", required=True, metavar="SHA256:...")
    vr.add_argument("--dispositions", metavar="FILE", help="human dispositions bound to the exact prior report")
    vr.add_argument("--operator-confirms-key-away", action="store_true",
                    help="operator states that the signing key is away; a second terminal YES is required")
    bp = sub.add_parser("baseline-prepare", help="prepare a no-signed-predecessor baseline package")
    bp.add_argument("--candidate", default="HEAD", metavar="SHA|REF")
    bp.add_argument("--approved-roster", required=True, metavar="FILE")
    bp.add_argument("--reader-record", required=True, metavar="FILE")
    bp.add_argument("--output-dir", required=True, metavar="DIR")
    bri = sub.add_parser("baseline-reader-inputs", help="prepare an unreviewed independent reader-record draft")
    bri.add_argument("--candidate", default="HEAD", metavar="SHA|REF")
    bri.add_argument("--approved-roster", required=True, metavar="FILE")
    bri.add_argument("--output", required=True, metavar="FILE")
    bi = sub.add_parser("baseline-install", help="install an independently reviewed forward baseline")
    bi.add_argument("--candidate", default="HEAD", metavar="SHA|REF")
    bi.add_argument("--package-dir", required=True, metavar="DIR")
    bi.add_argument("--approved-roster", required=True, metavar="FILE")
    bi.add_argument("--reader-record", required=True, metavar="FILE")
    bi.add_argument("--signing-key", required=True, metavar="PUBLIC-KEY")
    bi.add_argument("--expected-fingerprint", required=True, metavar="SHA256:...")
    bi.add_argument("--confirm-package-sha256", required=True, metavar="SHA256")
    args = ap.parse_args(argv)
    if args.verb in ("baseline-prepare", "baseline-reader-inputs"):
        saved_env = dict(os.environ)
        safe_home = tempfile.mkdtemp(prefix="repin-baseline-home-")
        safe_env = {key: os.environ[key] for key in ("PATH", "TMPDIR", "SYSTEMROOT")
                    if key in os.environ}
        safe_env.update(HOME=safe_home, LC_ALL="C", GIT_TERMINAL_PROMPT="0",
                        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        try:
            os.environ.clear()
            os.environ.update(safe_env)
            repo = Path(__file__).resolve().parent.parent
            if args.verb == "baseline-prepare":
                baseline_prepare(repo, args.candidate, args.approved_roster,
                                 args.reader_record, args.output_dir)
            else:
                baseline_reader_inputs(repo, args.candidate, args.approved_roster, args.output)
            return 0
        except (Refuse, OSError, ValueError, KeyError) as exc:
            print(f"\nrepin stopped; no authority changed.\n  {exc}", file=sys.stderr)
            return 2
        finally:
            os.environ.clear()
            os.environ.update(saved_env)
            shutil.rmtree(safe_home, ignore_errors=True)
    if args.verb == "baseline-install":
        try:
            baseline_install(Path(__file__).resolve().parent.parent, args.candidate,
                             args.package_dir, args.approved_roster, args.reader_record,
                             args.signing_key, args.expected_fingerprint,
                             args.confirm_package_sha256)
            return 0
        except (Refuse, OSError, ValueError, KeyError, RuntimeError) as exc:
            print(f"\nrepin stopped; no ref moved unless atomic install completed.\n  {exc}",
                  file=sys.stderr)
            return 2
    if args.verb == "prepare-values":
        try:
            prepare_values(Path(__file__).resolve().parent.parent, args.output, args.signing_key,
                           args.home, args.ceremony_dir)
            return 0
        except (Refuse, OSError, ValueError) as exc:
            print(f"\nrepin stopped; no authority changed.\n  {exc}", file=sys.stderr)
            return 2
    if args.verb in ("prepare-verifier", "verify-candidate"):
        try:
            if args.verb == "prepare-verifier":
                _verifier_prepare(args.trusted_repo, args.prior_anchor, args.candidate,
                                  args.trusted_ref, args.expected_fingerprint, args.evidence_dir)
                return 0
            return _verifier_run(args.evidence_dir, args.expected_fingerprint, args.dispositions,
                                 confirm_key_away=args.operator_confirms_key_away)
        except (Refuse, OSError, ValueError, KeyError) as exc:
            print(f"\nrepin stopped; no authority changed.\n  {exc}", file=sys.stderr)
            return 2
    tmp = Path(tempfile.mkdtemp(prefix="repin-"))
    rec, done = [], None
    try:
        repo = Path(__file__).resolve().parent.parent
        if args.verb in ("transition-packet", "prepare-reader"):
            prior = git_text(repo, "rev-parse", "--verify", ANCHOR_REF + "^{commit}")
            roster = tmp / "prior-roster"
            roster.write_bytes(git(repo, "cat-file", "blob", f"{prior}:{ROSTER_REL}"))
            if not re.fullmatch(r"SHA256:[A-Za-z0-9+/]{43}", args.expected_fingerprint):
                raise Refuse("supply the independently trusted SHA256 signing fingerprint.")
            good, _, _ = verify_checkpoint(repo, prior, roster, args.expected_fingerprint)
            if not good:
                raise Refuse("the prior anchor does not verify by the independently trusted fingerprint.")
            head = git_text(repo, "rev-parse", "--verify", "HEAD^{commit}")
            if git(repo, "cat-file", "blob", f"{head}:{REPIN_REL}") != Path(__file__).read_bytes():
                raise Refuse("the running preparation script differs from committed candidate C.")
        transition_ceremony = args.verb == "ceremony" and args.transition
        if args.verb == "ceremony" and args.transition and args.first_run:
            raise Refuse("--transition cannot be combined with --first-run.")
        if args.verb == "ceremony" and args.expected_fingerprint and not args.transition:
            raise Refuse("--expected-fingerprint is only used with --transition.")
        ctx = boot(repo, tmp, prior_authority=args.verb in ("transition-packet", "prepare-reader")
                   or transition_ceremony)
        first_screen(ctx)
        if args.verb == "status":
            show_ast(ctx, ast_view(ctx))
            say("  lockfile correction owed: " + ("no" if lockfile_correction(ctx) is None else "yes"))
            manifest_status(ctx, args.dropped_from)
        elif args.verb == "package":
            package(ctx, args.ceremony_dir, reviewed_deletions=args.delete_symbol)
        elif args.verb == "packet":
            build_packet(ctx, args.ceremony_dir)
        elif args.verb == "transition-packet":
            build_packet(ctx, args.ceremony_dir, transition=True)
        elif args.verb == "prepare-reader":
            prepare_reader_inputs(ctx, args.ceremony_dir, args.output)
        elif args.verb == "apply-reviewed-pin":
            apply_reviewed_pin(ctx, args.ceremony_dir)
        elif args.verb == "commit-reviewed-pin":
            commit_reviewed_pin(ctx, args.ceremony_dir)
        else:
            try:
                done = run_ceremony(ctx, args, launchctl, rec)
            finally:
                if Path(args.ceremony_dir).is_dir():
                    finish(ctx, *write_record(args.ceremony_dir, rec), done, rec)
        if args.verb not in ("ceremony", "apply-reviewed-pin", "commit-reviewed-pin"):
            check_head(ctx)
        return 0
    except Refuse as exc:
        print(f"\nrepin stopped; nothing was written.\n  {exc}", file=sys.stderr)
        return 2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        if Path(str(sys.pycache_prefix)).name.startswith("repin-pyc-"):
            shutil.rmtree(sys.pycache_prefix, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
