#!/usr/bin/env python3
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
# SPDX-License-Identifier: MIT
"""Re-pin checksums and re-anchor the gate, as one command a person runs.

``status`` reads and writes nothing: it shows what the engine's AST pin and
the gate manifest owe, and which commits touched the files involved.
``package`` computes the AST pin's transaction (the new baseline bytes, and the
known-new file when it must change), prints its digest and writes only into
``--ceremony-dir``.  The write itself, ``apply_pin``, never commits: it stops
after one ``yes`` and prints the ``git commit`` line.  ``ceremony`` runs the
whole re-anchor at a terminal: it compares the launcher's digest, checks the
packet, roster and anchor signature, refuses a signing key that is loaded in any
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


class Refuse(Exception):
    """A check failed.  The text says what happened, why, and what to do next."""


D = None  # the anchor's encode_display, loaded once the anchor is read


def d(value):
    """Text from git, files or children, made safe for a terminal."""
    if D is None:
        raise RuntimeError("the display encoder is not loaded")
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


def boot(repo, tmp):
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
    for rel in LISTED:
        got = sha((ext / rel).read_bytes()) if (ext / rel).is_file() else None
        if got != frozen.get(rel):
            raise Refuse(f"{rel} at HEAD does not equal the anchor's entry "
                         f"({got} against {frozen.get(rel)}). Its bytes decide what "
                         f"this tool runs, so nothing was imported. Only the by-hand "
                         f"ceremony in {RUNBOOK} anchors new bytes.")
    made = load_listed(ext, session_path)
    ctx = {k: sys.modules[v] for k, v in (("gm", "bootstrap.tests._gate_manifest"),
                                          ("gp", "bootstrap.tests._gate_preflight"),
                                          ("rc", "scripts.reanchor_ceremony"))}
    check_loaded(before, made, ext, frozen)
    running = Path(__file__).read_bytes()
    entry = frozen.get(REPIN_REL)
    at_head = (ext / REPIN_REL).read_bytes() if (ext / REPIN_REL).is_file() else None
    state = ("not committed at HEAD" if at_head is None else
             "anchored" if entry == sha(at_head) == sha(running) else
             "no anchored entry" if entry is None else "differs from the anchor")
    ctx.update(repo=repo, tmp=tmp, ext=ext, head=head, anchor=anchor, man=man,
               frozen=frozen, ents=ents, session_oid=session_oid, repin_state=state,
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
    say(f"checked  {len(LISTED)} files at HEAD equal the anchor's entries before any import; "
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


def render_changes(rel, old_raw, new_raw):
    """Every key the write changes, from the bytes on disk against the bytes to be
    written.  Not stored text and not the checker's classifier."""
    old, new = parse_output(rel, old_raw), parse_output(rel, new_raw)
    if rel == BASELINE_REL and set(old) != set(new):
        raise Refuse("the pin would add or drop a baseline key. That is a full "
                     "re-pin, which erases the motion record. Nothing was written.")
    fmt = lambda v: "(absent)" if v is None else json.dumps(v, sort_keys=True)
    return [f"  {Path(rel).name}  {d(k)}:  {d(fmt(old.get(k)))}  ->  {d(fmt(new.get(k)))}"
            for k in sorted(set(old) | set(new)) if old.get(k) != new.get(k)]


def build_transaction(ctx):
    """The AST pin as data: the new bytes of each output and what they replace.
    None when no pin is owed."""
    if ctx["closure_changed"]:
        raise Refuse("these authority files differ from the anchor: "
                     + ", ".join(d(m) for m in ctx["closure_changed"])
                     + ". That is a transition ceremony, not an AST pin.")
    view = ast_view(ctx)
    if view["missing"] or view["dup"]:
        raise Refuse("a baselined symbol is missing or defined twice. That is a review "
                     "item, never a pin. Run `status` and read the symbols named.")
    ext, new, files = ctx["ext"], {}, set()
    old = {rel: (ext / rel).read_bytes() for rel in OUTPUTS if (ext / rel).is_file()}
    if view["owed"]:
        base = json.loads(old[BASELINE_REL])
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
        files = {v[2] for v in view["changed"].values()}
        files |= {view["new_files"][k] for k in view["rekeyed"] + view["added"]}
    lock = lockfile_correction(ctx)
    if lock is not None:
        new[LOCKFILE_REL] = lock
    if not new:
        return None
    return {"schema": "repin-ast-transaction/v1", "head": ctx["head"], "anchor": ctx["anchor"],
            "influences": {"python": sys.version, "git_version": git_text(ctx["repo"], "--version"),
                           "display_encoder_blob": ctx["session_oid"]},
            "files": sorted(files),
            "outputs": {rel: {"preimage_blob": git_text(ctx["repo"], "rev-parse", f"{ctx['head']}:{rel}"),
                              "preimage_sha256": sha(old[rel]), "new_sha256": sha(raw),
                              "new_text": raw.decode()} for rel, raw in new.items()},
            "summary": [ln for rel, raw in new.items() for ln in render_changes(rel, old[rel], raw)]}


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


def store_txn(cdir, raw):
    cdir = Path(cdir)
    if cdir.is_symlink() or not cdir.is_dir():
        raise Refuse(f"the ceremony folder {d(str(cdir))} is not a plain folder.")
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


def check_preconditions(ctx):
    """Shared by `ceremony` step 2 and the apply step: refuse unless the tree is a
    clean, committed branch state that git can report on exactly."""
    repo, pin = ctx["repo"], ctx["man"]["interpreter"]["version_info"]
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
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


def apply_pin(ctx, cdir, raw):
    """`ceremony` step 5: write the AST pin this process just packaged, after one yes.
    Never commits.  *raw* is the transaction packaged in this very process."""
    check_preconditions(ctx)
    repo, head = ctx["repo"], ctx["head"]
    if read_safe(Path(cdir) / TXN_NAME, own=True) != raw:
        raise Refuse("the transaction file changed after it was packaged. Nothing was written.")
    txn = json.loads(raw)
    if txn["head"] != head or not txn["outputs"] or not set(txn["outputs"]) <= set(OUTPUTS):
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
        for line in render_changes(rel, disk, new):
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
    say(f"\nWritten, not committed. HEAD is still {head}.\nCommit exactly these paths:\n"
        f"  git commit {' '.join(blobs)} -m \"AST pin\"\nPut in the commit body: transaction "
        f"digest {digest}, python {sys.version.split()[0]}, new blob ids "
        + ", ".join(f"{Path(r).name} {b}" for r, b in blobs.items())
        + f".\nThen run ceremony again; its re-run check reads {record.name}.")
    return record


NOTHING_OWED = "\nNo pin is owed: the baseline accounts for the engine and the lockfile has nothing to correct."


def package(ctx, cdir=None):
    """The AST pin's transaction, its digest and (with a folder) the file; no repository write."""
    txn = build_transaction(ctx)
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


#: The launcher's two lines that tell a person to load the key with ssh-add, which this
#: key must never be; every other line, one that merely names ssh-add included, is relayed.
ADVICE = ("that is a missing key, not a broken tool", "ssh-add <your ceremony key>")


def is_advice(line):
    return any(text in line for text in ADVICE)


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
              "-c", f"gpg.ssh.program={KEYGEN}", "log", "-1", "--format=%G?%x00%GK", commit)
    status, _, key = out.decode().strip().partition("\0")
    return status == "G" and key == fingerprint, status, key


def anchor_state(ctx, roster):
    """('G', fp) good; ('N', ...) unsigned; anything else is a signature that fails."""
    ok, status, key = verify_checkpoint(ctx["repo"], ctx["anchor"], roster, None)
    return status, key


def last_signed(ctx, roster):
    rows = git(ctx["repo"], "-c", "gpg.format=ssh", "-c", f"gpg.ssh.allowedSignersFile={roster}",
               "-c", f"gpg.ssh.program={KEYGEN}", "log", "--first-parent", "-n", "2000",
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
    field = {k: rc.values_field(values, k) for k in ("checkout", "signing_key", "package", "home")}
    if None in field.values() or Path(field["checkout"]).resolve() != repo:
        raise Refuse("the values file must name checkout, signing_key, package and home, and its "
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
        pasted = input("\nPaste the launcher digest from the review's record: ").strip()
    except EOFError:
        pasted = ""
    say(f"  launcher {d(str(launcher))}\n  computed {ldigest}\n  pasted   {d(pasted)}")
    if pasted != ldigest:
        raise Refuse("the launcher's digest is not the one in the review's record. Do not run it.")
    rec.append(f"launcher digest {ldigest} equals the pasted digest")
    confirm(rec, "Do the two digests match?")

    def launcher_unchanged():
        """The launcher runs twice, minutes and a prompt apart; it is hashed before each run."""
        if sha(read_safe(launcher)) != ldigest:
            raise Refuse("the launcher changed after its digest was compared. Nothing further was run.")
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
    copy = tmp / "artifact" / "reanchor.sh"
    copy.parent.mkdir()
    copy.write_bytes(art)

    def artifact(command):
        if sha(copy.read_bytes()) != want:
            raise Refuse("the private copy of reanchor.sh changed since it was hashed.")
        env = {"PATH": CHILD_PATH, "HOME": field["home"], "LC_ALL": "C"}
        return child(rec, [SH, str(copy), command, str(values)], env=env)
    r = artifact("validate")
    if r.returncode:
        relay(r.stdout + r.stderr)
        raise Refuse("reanchor.sh validate refused the values file. No report was shown.")
    # 3. roster and anchor
    # The packet's member rows were compared with HEAD above, the roster's included,
    # so this copy is the roster the packet pins.
    roster = tmp / "roster"
    roster.write_bytes((ctx["ext"] / ROSTER_REL).read_bytes())
    fingerprint = key_fingerprint(rec, pub)
    rec.append(f"signing key fingerprint {fingerprint}")
    kt, kd = Path(pub).read_text().split()[:2]
    if not any(kt in t and kd in t and t.index(kd) == t.index(kt) + 1
               for t in (ln.split() for ln in roster.read_text().splitlines())):
        raise Refuse(f"the signing key {fingerprint} is not in the packet-pinned roster.")
    status, signer = anchor_state(ctx, roster)
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
    if ctx["closure_changed"]:
        raise Refuse("authority files differ from the anchor: " + ", ".join(d(m) for m in ctx["closure_changed"])
                     + f". That is a transition ceremony. Run it by hand under {RUNBOOK}.")
    if args.first_run:
        check_first_run(ctx, args.reviewed_commit)
    elif args.reviewed_commit or ctx["repin_state"] != "anchored":
        raise Refuse(f"{REPIN_REL} is {ctx['repin_state']}; its bytes are not the anchor's. Only the "
                     f"first run may continue, with --first-run --reviewed-commit <id>.")
    check_stop_records(ctx, cdir, args.first_run)
    key_checks(rec, pub, private, fingerprint, launchctl, "before stage 1")
    # 5. an owed pin is written, then this stops (a first run shows a lockfile correction and leaves it)
    raw = None if args.first_run else package(ctx, cdir)
    if raw:
        apply_pin(ctx, cdir, raw)
        rec.append("yes typed on a terminal: Write these files? (AST pin)")
        return None, None
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
    theirs = [t for t in artifact("hash-package").stdout.split() if len(t) == 64 and t.isalnum()]
    if theirs[:1] != [own]:
        raise Refuse("the launcher's hash of the package and this program's disagree.")
    say("\nSummary 2: what you are about to sign")
    relay(artifact("show-report").stdout)
    manifest_status(ctx)
    say(f"authority files changed since the anchor: 0 of {len(ctx['closure'])}\n"
        f"anchor signature: {'good, by a roster key' if status == 'G' else 'unsigned (first run)'}\n"
        f"signing key fingerprint: {fingerprint}\npackage digest: {own}")
    rec.append(f"package digest {own}")
    confirm(rec, "Does Summary 2 describe what you intend to sign?")
    if sha(read_safe(package_file)) != own:
        raise Refuse("the package was rewritten after you read the report. Nothing was signed.")
    # 8-9. (signing path) key checks again, then stage 2 with the terminal attached and a short environment
    key_checks(rec, pub, private, fingerprint, launchctl, "before stage 2")
    note = ("The launcher's advice to load the key with ssh-add does not apply here: this key must "
            "never be loaded into an agent.")
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
        if not is_advice(line):
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


def main(argv=None, *, launchctl=launchctl_socket):
    ap = argparse.ArgumentParser(prog="repin", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    st = sub.add_parser("status", help="show what the pins owe; writes nothing")
    st.add_argument("--dropped-from", metavar="FILE", help="the saved text of a "
                    "`_gate_manifest.py verify` run, to sort its dropped test nodes")
    pk = sub.add_parser("package", help="compute the AST pin's transaction and print its "
                        "digest; writes only into --ceremony-dir")
    pk.add_argument("--ceremony-dir", metavar="DIR", help="a folder to keep the transaction in")
    ce = sub.add_parser("ceremony", help="the whole re-anchor: checks, an owed AST pin (then stop), "
                        "the launcher's two stages, verification")
    ce.add_argument("--values", required=True, metavar="FILE", help="your values file")
    ce.add_argument("--ceremony-dir", required=True, metavar="DIR", help="holds the packet and "
                    "launcher, and receives the transaction, stop record and record")
    ce.add_argument("--first-run", action="store_true", help="the anchor does not pin this tool yet")
    ce.add_argument("--reviewed-commit", metavar="ID", help="with --first-run: the last commit the "
                    "code reviewer read that edited this tool or its tests")
    args = ap.parse_args(argv)
    tmp = Path(tempfile.mkdtemp(prefix="repin-"))
    rec, done = [], None
    try:
        ctx = boot(Path(__file__).resolve().parent.parent, tmp)
        first_screen(ctx)
        if args.verb == "status":
            show_ast(ctx, ast_view(ctx))
            say("  lockfile correction owed: " + ("no" if lockfile_correction(ctx) is None else "yes"))
            manifest_status(ctx, args.dropped_from)
        elif args.verb == "package":
            package(ctx, args.ceremony_dir)
        else:
            try:
                done = run_ceremony(ctx, args, launchctl, rec)
            finally:
                if Path(args.ceremony_dir).is_dir():
                    finish(ctx, *write_record(args.ceremony_dir, rec), done, rec)
        if args.verb != "ceremony":
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
