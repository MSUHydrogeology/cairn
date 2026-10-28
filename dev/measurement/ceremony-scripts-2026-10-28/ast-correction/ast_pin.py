#!/usr/bin/env python3.13
"""One-off correction: pin the engine's AST fixtures while dropping four reviewed deletions.

`repin` refuses to pin a deleted baseline symbol.  So this script (1) removes
exactly those four keys in a THROWAWAY git worktree, (2) lets `repin package`
compute the corrected fixtures there, (3) checks the result against what
`repin status` lists in the real repo, and (4) with --apply only, writes the two
fixture files into the real working tree.  Dry run is the default.  It never
commits, signs, loads a key, runs a ceremony or touches another file."""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

BASE = "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
KNOWN = "bootstrap/tests/fixtures/scaffold_ast_known_new.json"
DELETED = {"Assign:_ONBOARDING_HELPER_DST_REL", "Assign:_ONBOARDING_HELPER_SRC_REL",
           "Assign:_ONBOARDING_LOG_HEADER", "Assign:_ONBOARDING_LOG_REL"}
DELETING_COMMIT = "fa86e2cb"  # "Onboarding at install, C4: remove the helper and the always-on group"
ENGINE = "bootstrap/_scaffold"
COMMIT_MSG = "ast-attest: pin the engine after the 0.5 changes; four reviewed deletions"


class Stop(Exception):
    """A refusal.  Nothing has been written to the real repository."""


def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(obj): return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()  # repin's own format


def run(argv, cwd, check=True):
    env = {**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
           "PYTHONDONTWRITEBYTECODE": "1", "GIT_TERMINAL_PROMPT": "0"}
    r = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True)
    if check and r.returncode:
        raise Stop(f"`{' '.join(map(str, argv[:4]))} ...` failed (exit {r.returncode}): {(r.stderr or r.stdout).strip()[-600:]}")
    return r


def git(repo, *a, check=True):
    return run(["git", "-C", str(repo), "-c", "core.hooksPath=/dev/null", *a], repo, check)


def parse_status(text):
    """Sort the symbol lines of `repin status` into the six classes it prints."""
    out = {k: set() for k in ("changed", "missing", "dup", "rekeyed", "added", "dropped")}
    pat = {"changed": r"^  CHANGED  (\S+)", "missing": r"^  MISSING  (\S+)", "dup": r"^  DUPLICATE  (\S+)",
           "rekeyed": r"^  known-new REKEYED  (\S+)", "added": r"^  known-new ADDED  (\S+)",
           "dropped": r"^  known-new DROPPED  (\S+)"}
    for line in text.splitlines():
        for k, p in pat.items():
            m = re.match(p, line)
            if m: out[k].add(m.group(1))
    return out


def prove_deletion(repo, key, deleting):
    """Why dropping `key` is a deletion and not a loss: it is gone from the live engine, its last
    change was the reviewed commit, and that commit's parent still had it."""
    name = key.split(":", 1)[1]
    live = git(repo, "grep", "-c", "-w", "-e", name, "HEAD", "--", ENGINE, check=False)
    if live.returncode != 1 or live.stdout.strip():
        raise Stop(f"{key} is still mentioned in the engine at HEAD, so it is not a deletion.")
    last = git(repo, "log", "-n1", "--format=%H", f"-S{name}", "HEAD", "--", ENGINE).stdout.strip()
    if last != deleting:
        raise Stop(f"the latest commit touching {name} is {last[:10]}, not the expected {deleting[:10]}.")
    if git(repo, "grep", "-c", "-w", "-e", name, f"{deleting}^", "--", ENGINE, check=False).returncode != 0:
        raise Stop(f"{name} was not present just before {deleting[:10]}, so that commit did not delete it.")
    return f"{key}: absent from the engine at HEAD; last touched by {last[:10]}, which removed it"


def check_txn(txn, scratch_head, old_base, old_known, status):
    """Hold repin's transaction to exactly what `repin status` listed.  Returns the summary."""
    if txn.get("schema") != "repin-ast-transaction/v1" or txn.get("head") != scratch_head:
        raise Stop("repin's transaction has an unexpected schema or was computed at another commit.")
    if set(txn["outputs"]) != {BASE, KNOWN}:  # e.g. a lockfile correction would show up here
        raise Stop("repin's transaction writes unexpected files: " + ", ".join(sorted(set(txn["outputs"]) ^ {BASE, KNOWN})))
    new = {}
    for rel, o in txn["outputs"].items():
        raw = o["new_text"].encode()
        if sha(raw) != o["new_sha256"] or dump(json.loads(raw)) != raw:
            raise Stop(f"{rel}: the new text does not match its digest or repin's format.")
        new[rel] = (raw, json.loads(raw))
    nb, nk = new[BASE][1], new[KNOWN][1]
    kept = {k: v for k, v in old_base.items() if k not in DELETED}
    if set(nb) != set(kept):
        raise Stop("the corrected baseline's key set is not the old one minus the four deletions.")
    got = {"changed": {k for k in nb if nb[k] != kept[k]},
           "rekeyed": {k for k in nk if k in old_known and nk[k] != old_known[k]},
           "added": set(nk) - set(old_known), "dropped": set(old_known) - set(nk)}
    for cls, keys in got.items():
        if keys != status[cls]:
            raise Stop(f"{cls.upper()}: repin's transaction touches {sorted(keys ^ status[cls])} "
                       f"that `repin status` does not agree on.")
    return got, {rel: raw for rel, (raw, _) in new.items()}, len(old_base), len(nb)


def attest_ok(root, baseline, known):
    """The repository's own checker, over the engine, with the known-new manifest enforced."""
    mods = sorted(str(p) for p in (Path(root) / ENGINE).glob("*.py"))
    r = run([sys.executable, "-I", "-B", Path(root) / "bootstrap/tests/_ast_attest.py", "verify",
             baseline, "--known-new", known, *mods], root, check=False)
    if r.returncode or "AST attestation OK" not in r.stdout:
        raise Stop("_ast_attest verify did not end 'AST attestation OK':\n" + (r.stderr or r.stdout)[-800:])
    return r.stdout.strip()


def build(repo, deleting, work):
    """Everything up to (not including) any write to the real repo.  Returns the report data."""
    head = git(repo, "rev-parse", "--verify", "HEAD^{commit}").stdout.strip()
    if git(repo, "merge-base", "--is-ancestor", deleting, head, check=False).returncode:
        raise Stop(f"{deleting[:10]} is not an ancestor of HEAD.")
    blobs = {rel: git(repo, "show", f"HEAD:{rel}").stdout.encode() for rel in (BASE, KNOWN)}
    for rel in blobs:  # we analyse HEAD; the files we may replace must still be HEAD's
        if (Path(repo) / rel).read_bytes() != blobs[rel]:
            raise Stop(f"{rel} in the working tree differs from HEAD. Commit or discard that first.")
    old_base, old_known = json.loads(blobs[BASE]), json.loads(blobs[KNOWN])
    if dump(old_base) != blobs[BASE]:
        raise Stop("the baseline does not round-trip through repin's format, so a rewrite would change unrelated bytes.")
    status_out = run([sys.executable, Path(repo) / "scripts/repin.py", "status"], repo, check=False)
    if status_out.returncode:
        raise Stop("`repin status` refused:\n" + status_out.stderr.strip())
    status = parse_status(status_out.stdout)
    if status["missing"] != DELETED or status["dup"]:   # a fifth missing or any duplicate is a review item
        raise Stop(f"the missing set is {sorted(status['missing'])} (duplicates {sorted(status['dup'])}); "
                   f"expected exactly the four named deletions.")
    proofs = [prove_deletion(repo, k, deleting) for k in sorted(DELETED)]
    wt = Path(work) / "wt"
    git(repo, "worktree", "add", "--detach", str(wt), head)
    (wt / BASE).write_bytes(dump({k: v for k, v in old_base.items() if k not in DELETED}))
    c = ["-c", "commit.gpgsign=false", "-c", "user.name=scratch", "-c", "user.email=scratch@invalid"]
    git(wt, *c, "commit", "--no-verify", "-q", "-m", "scratch: four baseline keys removed", BASE)
    scratch_head = git(wt, "rev-parse", "HEAD").stdout.strip()
    if (wt / "scripts/repin.py").read_bytes() != (Path(repo) / "scripts/repin.py").read_bytes():
        raise Stop("scripts/repin.py differs between the real repo and HEAD.")
    cdir = Path(work) / "cdir"; cdir.mkdir()
    pk = run([sys.executable, wt / "scripts/repin.py", "package", "--ceremony-dir", cdir], wt, check=False)
    if pk.returncode:
        raise Stop("`repin package` refused in the scratch worktree:\n" + pk.stderr.strip())
    txn = json.loads((cdir / "ast-pin-transaction.json").read_bytes())
    got, new, n_before, n_after = check_txn(txn, scratch_head, old_base, old_known, status)
    fixed = Path(work) / "fixed"; fixed.mkdir()
    for rel, raw in new.items():
        (fixed / Path(rel).name).write_bytes(raw)
    verdict = attest_ok(wt, fixed / Path(BASE).name, fixed / Path(KNOWN).name)
    return dict(head=head, proofs=proofs, got=got, new=new, n_before=n_before, n_after=n_after, verdict=verdict, status=status)


def report(r):
    p = print
    p("Four baseline symbols were deleted from the engine, and each deletion checks out:")
    for line in r["proofs"]: p("  " + line)
    g = r["got"]
    p(f"\nBaseline keys: {r['n_before']} before, {r['n_after']} after (the four deleted ones removed).")
    p(f"Updated baseline entries (CHANGED): {len(g['changed'])}   known-new ADDED {len(g['added'])}, "
      f"REKEYED {len(g['rekeyed'])}, DROPPED {len(g['dropped'])}")
    p("These counts and the symbol names are IDENTICAL to what `repin status` lists: YES (checked by name).")
    for cls in ("changed", "rekeyed", "added", "dropped"):
        p(f"  {cls}: " + ", ".join(sorted(g[cls])))
    p("\nCorrected fixtures (sha256):")
    for rel, raw in r["new"].items(): p(f"  {sha(raw)}  {rel}")
    p("\nIn a scratch copy with these fixtures: " + r["verdict"])


def apply(repo, r):
    """Write the two files atomically, re-verify in the real tree, then say how to commit."""
    old = {}
    for rel, raw in r["new"].items():
        dst = Path(repo) / rel
        old[dst] = dst.read_bytes()
        tmp = dst.with_name(dst.name + ".ast-pin.tmp")
        tmp.write_bytes(raw); os.replace(tmp, dst)
    try:
        print("\nWritten. Real tree: " + attest_ok(repo, Path(repo) / BASE, Path(repo) / KNOWN))
        t = run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "bootstrap/tests/test_ast_attest.py", "-q"], repo, check=False)
        print(t.stdout.strip().splitlines()[-1] if t.stdout.strip() else t.stderr.strip())
        if t.returncode: raise Stop("test_ast_attest.py failed.")
    except Stop:
        for dst, raw in old.items(): dst.write_bytes(raw)  # put HEAD's bytes back
        raise
    print(f"\nNothing is committed. To commit exactly these two files:\n  git commit {BASE} {KNOWN} -m \"{COMMIT_MSG}\"")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true", help="write the two fixtures into the real working tree")
    ap.add_argument("--repo", default=None, help="the repository (default: the one you are in)")
    ap.add_argument("--deleted-by", default=DELETING_COMMIT, help="the commit that deleted the four symbols")
    a = ap.parse_args(argv)
    work, repo = tempfile.mkdtemp(prefix="ast-pin-"), None
    try:
        if sys.version_info[:2] != (3, 13): raise Stop("run this with Python 3.13 (the digests differ across minors).")
        repo = Path(git(a.repo or os.getcwd(), "rev-parse", "--show-toplevel").stdout.strip())
        deleting = git(repo, "rev-parse", "--verify", a.deleted_by + "^{commit}").stdout.strip()
        r = build(repo, deleting, work)
        report(r)
        if git(repo, "rev-parse", "HEAD").stdout.strip() != r["head"]: raise Stop("HEAD moved while this ran.")
        if a.apply: apply(repo, r)
        else: print("\nDRY RUN: nothing was written. Run again with --apply to write the two fixtures.")
        return 0
    except Stop as e:
        print(f"\nast_pin stopped; nothing was written to the repository.\n  {e}", file=sys.stderr)
        return 2
    finally:
        if repo is not None and (Path(work) / "wt").exists():
            git(repo, "worktree", "remove", "--force", str(Path(work) / "wt"), check=False)
            git(repo, "worktree", "prune", check=False)
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
