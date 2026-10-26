#!/usr/bin/env python3
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
# SPDX-License-Identifier: MIT
"""Re-pin checksums and re-anchor the gate, as one command a person runs.

``status`` reads and writes nothing: it shows what the engine's AST pin and
the gate manifest owe, and which commits touched the files involved.  Nothing
runs this unprompted.

Every check reads the committed tree (``HEAD``), never the working tree: the
files are extracted from raw git objects, the code this process runs is
compared byte for byte with the signed anchor's manifest before it is
imported, and the process itself runs isolated (``-I``) with a fresh bytecode
folder.  A same-user edit to this file is outside what it can detect.
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
import hashlib
import importlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sysconfig
import tempfile
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
    # Append, never insert: appended, the standard library wins a name clash.
    sys.path.append(str(ext))
    mods = {"gm": "bootstrap.tests._gate_manifest", "gp": "bootstrap.tests._gate_preflight",
            "rc": "scripts.reanchor_ceremony"}
    ctx = {k: importlib.import_module(v) for k, v in mods.items()}
    stdlib = [os.path.realpath(sysconfig.get_path(k)) for k in ("stdlib", "platstdlib")]
    for name in sorted(set(sys.modules) - before):
        f = getattr(sys.modules[name], "__file__", None)
        if not f or os.path.realpath(f) == str(session_path.resolve()):
            continue
        f = os.path.realpath(f)
        if "site-packages" not in f and any(f.startswith(s + os.sep) for s in stdlib):
            continue
        rel = os.path.relpath(f, ext.resolve())
        if rel not in LISTED or sha(Path(f).read_bytes()) != frozen[rel]:
            raise Refuse(f"the module {name} loaded from {d(f)}, which is not on the "
                         f"checked list. Nothing further ran.")
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
root, mods = sys.argv[1], sys.argv[2:]
sys.path.append(root + "/bootstrap/tests")
import _ast_attest as A
fx = root + "/bootstrap/tests/fixtures/"
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


def ast_view(ctx):
    """Run the AST comparison in a child: isolated, fresh bytecode folder."""
    prefix = tempfile.mkdtemp(dir=ctx["tmp"], prefix="pyc-")
    r = subprocess.run([sys.executable, "-I", "-X", f"pycache_prefix={prefix}", "-c",
                        _AST_CHILD, str(ctx["ext"]), *ctx["engine"]], cwd=ctx["tmp"],
                       env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, capture_output=True)
    if r.returncode:
        raise Refuse(f"the AST comparison failed: {d(r.stderr.strip())}")
    out = json.loads(r.stdout)
    if not out["isolated"] or out["prefix"] != prefix:
        raise Refuse("the AST child did not run isolated with the fresh bytecode folder.")
    old = json.loads((ctx["ext"] / KNOWN_NEW_REL).read_bytes())
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


def main(argv=None):
    ap = argparse.ArgumentParser(prog="repin", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    st = sub.add_parser("status", help="show what the pins owe; writes nothing")
    st.add_argument("--dropped-from", metavar="FILE", help="the saved text of a "
                    "`_gate_manifest.py verify` run, to sort its dropped test nodes")
    args = ap.parse_args(argv)
    tmp = Path(tempfile.mkdtemp(prefix="repin-"))
    try:
        ctx = boot(Path(__file__).resolve().parent.parent, tmp)
        first_screen(ctx)
        show_ast(ctx, ast_view(ctx))
        manifest_status(ctx, args.dropped_from)
        check_head(ctx)
        return 0
    except Refuse as exc:
        print(f"\nrepin stopped; nothing was written.\n  {exc}", file=sys.stderr)
        return 2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
