#!/usr/bin/env python3
"""Read-only preflight for the gate-anchor re-anchor ceremony.

WHAT THIS ANSWERS, and it is the whole scope: *would the ceremony clear, and
what exactly would it move?* Both questions are pure functions of the tree, so
both can be answered before the ceremony key comes out of storage and before an
authorization package is spent. An operator who learns at stage 1 that the state
is refused has paid a full authorization package to be told something that was
free.

WITHOUT ``--run`` IT RUNS NO STAGE: it reports, and prints the commands. With
``--run`` it performs them, under three conditions an adversarial review of an
earlier version established the hard way.

**One: it never renders the report from unverified bytes.** The runbook's
``reanchor.sh show-report`` reads the working-tree artifact, which nothing has
checked at that point. Here the artifact is hashed against the packet's
``artifact_sha256`` first, and a mismatch refuses.

**Two: it never manufactures the confirmation.** Stage 2 asks the operator to
supply the package digest, and the artifact says why: no digest inside the
package can satisfy it, because a package can carry its own digest. An earlier
version computed that number and passed it, so stage 2 compared the driver's
arithmetic against the driver's arithmetic -- tautologically true, and the one
check requiring a human act could no longer fail. Now the digest is computed
**twice, by two different programs** -- the ceremony's own ``hash-package`` and
this tool's ``hashlib`` -- both are shown, and a disagreement refuses. That is
two sources on one machine, which is what one machine can honestly offer. It is
not an out-of-band third party and this tool does not pretend it is.

**Three: no exit status is discarded.** The earlier version printed "the report
below is the state your signature will bind", ignored a non-zero exit, and asked
for confirmation of a report that was never rendered.

IT NEVER TOUCHES KEY MATERIAL, and it NEVER PUSHES.

IT WRITES NOTHING INSIDE THE REPOSITORY -- with one disclosed exception, below.

THE EXCEPTION, STATED UP FRONT BECAUSE IT IS THE ONE THING A READER WOULD
OTHERWISE GET WRONG. The ceremony's own check has two halves. `check()` is pure.
`gather_evidence()` is not: it materializes the candidate tree to a temporary
directory and runs a pytest collection over it, which imports the candidate's
`conftest.py` and every test module. **That executes candidate code**, with
filesystem, process and network access -- the module says so itself, in a
banner it writes on every run, and Cairn accepts the residual under its
trusted-contributor model. This tool prints that banner rather than swallowing
it. Do not point `--candidate` at a branch you have not read.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ANCHOR_REF = "refs/cairn/gate-anchor"
ARTIFACT_REL = "bootstrap/reanchor.sh"
PACKET_SLOT = "@PACKET_SHA256@"
REVIEW_MANIFEST_SCHEMA = "cairn-review-manifest/v1"


def rule(char: str = "-") -> str:
    return char * 78


def head(title: str) -> None:
    print(f"\n{rule('=')}\n{title}\n{rule('=')}")


def say(text: str = "") -> None:
    print(text)


def stop(message: str, code: int = 2) -> None:
    say(f"\nSTOP: {message}")
    raise SystemExit(code)


# ---------------------------------------------------------------------------
# git, read sterilely
# ---------------------------------------------------------------------------
#
# The runbook records two reproduced failures this guards against: an inherited
# ``GIT_DIR`` redirected ``cat-file`` away from the explicitly named ``-C``
# checkout to a second repository and returned 0 (FUR7), and a replacement ref
# configured inside the candidate was honoured by the very command that would
# have discovered it (FUR6). This tool establishes nothing authoritative, so
# neither failure could cause a bad blessing here -- but a preflight that read a
# different repository than the ceremony would report a clean state for a tree
# nobody is about to bless, which is the silent kind of wrong.

_STERILE_ENV = {
    "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
    "HOME": "/nonexistent",
    "LC_ALL": "C",
}
_STERILE_FLAGS = [
    "--no-replace-objects",
    "-c", "core.useReplaceRefs=false",
    "-c", "core.hooksPath=/dev/null",
    "-c", "core.fsmonitor=false",
]


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *_STERILE_FLAGS, "-C", str(repo), *args],
        capture_output=True, text=True, env=_STERILE_ENV, check=False,
    )
    if result.returncode != 0:
        if not check:
            return ""
        stop(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def blob_at(repo: Path, rev: str, rel: str) -> bytes | None:
    result = subprocess.run(
        ["git", *_STERILE_FLAGS, "-C", str(repo), "cat-file", "blob", f"{rev}:{rel}"],
        capture_output=True, env=_STERILE_ENV, check=False,
    )
    return result.stdout if result.returncode == 0 else None


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    """Over the bytes on disk -- never over what a file says about itself."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# the values file -- two fields, positionally, and NOT a validating parse
# ---------------------------------------------------------------------------
#
# The launcher's reader and the artifact's reader are the two parsers of this
# grammar, bound by a parity test. A third would be a third thing to drift, so
# this reads the two fields it needs to know WHERE to look and validates
# nothing. `reanchor.sh validate <values>` is the check.

def values_field(values: Path, key: str) -> str | None:
    for line in values.read_text().splitlines():
        if line.startswith(f"{key} "):
            return line[len(key) + 1:]
    return None


TEMPLATE_REL = "bootstrap/reanchor-launcher.template.sh"


def closure_members(repo: Path, candidate: str) -> list[str]:
    """The closure, read from the reviewed launcher template's own fixed list.

    Not restated here: a second list is a second thing to drift, and the
    template is the reviewed statement of what the closure consists of.

    Read from the OBJECT STORE at the candidate, not from the working tree. The
    template is the pre-candidate trust root and is NOT itself a closure member,
    so nothing in this repository pins it; naming the commit is the only thing
    that makes these bytes identifiable to a reviewer.
    """
    blob = blob_at(repo, candidate, TEMPLATE_REL)
    if blob is None:
        stop(f"the candidate has no blob at {TEMPLATE_REL}")
    text = blob.decode()
    marker = "EXPECTED_PATHS='"
    try:
        start = text.index(marker) + len(marker)
        end = text.index("'", start)
    except ValueError:
        stop(f"cannot find EXPECTED_PATHS in {template}")
    return [line for line in text[start:end].splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# what would move
# ---------------------------------------------------------------------------

def compare(repo: Path, candidate: str, packet: Path | None) -> dict:
    """Print the closure three ways: at the anchor, at the candidate, in the packet.

    Three columns because three different questions are being asked, and
    collapsing them hides which one failed.

    * anchor vs candidate -- the TRANSITION. Expected; it is why the ceremony runs.
    * packet vs candidate -- a DEFECT. The launcher starts no artifact whose
      bytes it was not given, so a disagreement here is a refusal waiting to
      happen.
    """
    anchor_oid = git(repo, "rev-parse", ANCHOR_REF)
    members = closure_members(repo, candidate)

    # Parse ALL packet rows first, so a MISSING row is visible as missing.
    # Deciding "the packet matches" over only the rows that happen to be
    # present measures the intersection and reports it as the whole -- a packet
    # with no member rows at all would satisfy it.
    packet_rows: dict[str, str] = {}
    packet_extra: list[str] = []
    if packet is not None and packet.exists():
        for line in packet.read_text().splitlines():
            if line.startswith("member "):
                _, digest, rel = line.split(" ", 2)
                packet_rows[rel] = digest
        packet_extra = sorted(set(packet_rows) - set(members))

    template_blob = blob_at(repo, candidate, TEMPLATE_REL)
    say(f"\n  repository  {repo}")
    say(f"  template    {sha256_bytes(template_blob)[:12]}  "
        f"(read from {candidate[:12]}:{TEMPLATE_REL})")
    say(f"  anchor      {anchor_oid}")
    say(f"  candidate   {candidate}")
    say(f"  distance    {git(repo, 'rev-list', '--count', f'{anchor_oid}..{candidate}')}"
        f" commits from the anchor to the candidate")
    say("")
    say(f"  {'closure member':<38} {'anchor':<14} {'candidate':<14} packet")
    say(f"  {rule()}")

    rows, changed, bad = {}, [], []
    for rel in members:
        cand_blob = blob_at(repo, candidate, rel)
        if cand_blob is None:
            stop(f"the candidate has no blob at {rel}")
        cand = sha256_bytes(cand_blob)
        rows[rel] = cand

        anch_blob = blob_at(repo, anchor_oid, rel)
        anch = sha256_bytes(anch_blob) if anch_blob is not None else None
        if anch != cand:
            changed.append(rel)

        if packet is None or not packet.exists():
            pkt_col = "-"
        elif rel not in packet_rows:
            pkt_col = "MISSING !!"
            bad.append(f"{rel}: the packet has no row for this member")
        elif packet_rows[rel] != cand:
            pkt_col = f"{packet_rows[rel][:12]} !!"
            bad.append(f"{rel}: packet says {packet_rows[rel][:12]}, "
                       f"candidate is {cand[:12]}")
        else:
            pkt_col = "same"

        mark = " " if anch == cand else "*"
        anch_col = "(absent)" if anch is None else anch[:12]
        say(f" {mark}{rel:<38} {anch_col:<14} {cand[:12]:<14} {pkt_col}")

    say(f"  {rule()}")
    say(f"  * = differs from the anchor. {len(changed)} of {len(members)} members changed.")
    if changed:
        say("    This is a TRANSITION ceremony: it carries a closure change, and")
        say("    the launcher measures that for itself rather than being told.")

    for rel in packet_extra:
        bad.append(f"{rel}: the packet names a member the closure does not")

    return {"anchor": anchor_oid, "candidate": candidate, "members": rows,
            "changed": changed, "packet_problems": bad,
            "packet_present": packet is not None and packet.exists()}


def check_packet_pair(state: dict, packet: Path, launcher: Path) -> bool:
    """Do the packet and the launcher form the pair the launcher will demand?"""
    head("The operative materials")
    if not packet.exists():
        say(f"\n  packet    {packet}   ABSENT")
        say(f"  launcher  {launcher}   "
            f"{'present' if launcher.exists() else 'ABSENT'}")
        say("\n  Without both, the ceremony cannot start. They are produced")
        say("  together and travel together.")
        return False
    if not launcher.exists():
        say(f"\n  launcher {launcher} is ABSENT while the packet is present.")
        return False

    packet_digest = sha256_file(packet)
    launcher_text = launcher.read_text()
    say(f"\n  packet    {packet}")
    say(f"            sha256 {packet_digest}")
    say(f"  launcher  {launcher}")
    say(f"            sha256 {sha256_file(launcher)}")

    ok = True
    if PACKET_SLOT in launcher_text:
        say(f"\n  !! the launcher still carries the unfilled {PACKET_SLOT} slot.")
        say("     It will refuse: the placeholder is not 64 hex characters.")
        ok = False
    elif f"'{packet_digest}'" not in launcher_text:
        say("\n  !! the launcher does not carry this packet's digest.")
        say("     RA-02 compares the packet on disk against the digest bound")
        say("     into the launcher; that comparison is what makes them a pair,")
        say("     and it will fail.")
        ok = False
    else:
        say("\n  The launcher carries this packet's digest, so RA-02's pair")
        say("  comparison will hold. Verifying the launcher's digest against")
        say("  the record that produced it covers the packet too.")

    if PACKET_SLOT not in launcher_text:
        has_fix = "unset L_checkout" in launcher_text
        say("")
        if has_fix:
            say("  The launcher carries the environment-injection fix"
                " (unset L_*).")
        else:
            say("  !! THIS LAUNCHER PREDATES THE ENVIRONMENT-INJECTION FIX.")
            say("     It has no `unset L_*` in its values reader, so an exported")
            say("     L_shasum / L_git / L_python in the environment satisfies")
            say("     its missing-key check exactly as a values-file line does,")
            say("     and that program then runs inside the pre-candidate")
            say("     window. Reproduced 2026-08-27. DO NOT RUN THIS FILE.")
            ok = False

    for problem in state["packet_problems"]:
        say(f"  !! {problem}")
        ok = False
    return ok


# ---------------------------------------------------------------------------
# the rehearsal
# ---------------------------------------------------------------------------

def rehearse(repo: Path, state: dict) -> bool:
    head("The read-only rehearsal")
    say("""
  READ THIS BEFORE IT RUNS. The ceremony's check has two halves, and only one
  of them is pure.

    check()           pure. Reads the tree, decides, writes nothing.
    gather_evidence() NOT pure. It materializes the candidate tree to a
                      temporary directory and runs a pytest collection over
                      it, which imports the candidate's conftest.py and every
                      test module. THAT EXECUTES CANDIDATE CODE, with
                      filesystem, process and network access.

  Cairn accepts that residual under its trusted-contributor model, and stage 1
  does exactly the same thing. But this tool will not call it "read-only" when
  the module itself refuses to. Its banner is printed below rather than
  swallowed.""")

    sys.path.insert(0, str(repo / "bootstrap" / "tests"))
    try:
        import _gate_preflight as gp
    except Exception as exc:
        stop(f"cannot load the preflight module: {exc}")
    finally:
        sys.path.pop(0)

    import tempfile

    lines = [f"schema {REVIEW_MANIFEST_SCHEMA}",
             f"candidate {state['candidate']}",
             "provenance read-only rehearsal -- authorizes nothing"]
    lines += [f"member {d} {r}" for r, d in sorted(state["members"].items())]

    manifest_path = None
    try:
        transition = None
        if state["changed"]:
            with tempfile.NamedTemporaryFile("w", suffix=".manifest",
                                             delete=False) as fh:
                fh.write("\n".join(lines) + "\n")
                manifest_path = Path(fh.name)
            try:
                parsed, _ = gp.read_review_manifest(manifest_path)
                transition = gp.revalidate_transition(
                    parsed, state["candidate"], gp._resolve("HEAD", repo=repo),
                    anchor=state["anchor"], repo=repo)
            except Exception as exc:
                say(f"\n  the transition does not revalidate: {exc}")
                return False
            say(f"\n  transition revalidates against a manifest built here"
                f" ({len(transition['members'])} members).")
            say("  This is the driver checking its own arithmetic, not an")
            say("  independent confirmation: the real manifest is composed by")
            say("  the launcher from the packet, and this one authorizes nothing.")

        say(f"\n  {rule()}")
        try:
            evidence = gp.gather_evidence(state["candidate"], repo=repo,
                                          out=sys.stdout)
        except Exception as exc:
            say(f"\n  gather_evidence refused: {exc}")
            return False
        say(f"  {rule()}")

        report = gp.check(
            repo=repo, evidence=evidence,
            admitted_authority=(transition["members"] if transition else None))
    finally:
        if manifest_path is not None:
            manifest_path.unlink(missing_ok=True)

    say("")
    for finding in report.findings:
        say(f"  [{finding.level:<6}] {finding.code:<10} {finding.message}")
    if not report.findings:
        say("  (no findings)")

    say("")
    if report.blocked:
        say("  VERDICT: the read-only checks REFUSE this state.")
        say("  Resolve the findings marked 'refuse' before running the ceremony.")
        return False

    say("  VERDICT: the read-only checks CLEAR this state.")
    say("")
    say("  WHAT THAT DOES AND DOES NOT ESTABLISH. This ran the transition")
    say("  revalidation, the evidence gather and the read-only check. Stage 1")
    say("  runs more than that, and any of the rest can still stop the")
    say("  ceremony -- this list is what is known to be outside the rehearsal,")
    say("  not a proof that nothing else exists:")
    say("")
    say("    * the values file parse and every path predicate in it")
    say("      -> rehearsable: run `reanchor.sh validate <values>`")
    say("    * the signing key's own validation (that it parses, and that its")
    say("      fingerprint is in allowed_signers)")
    say("      -> rehearsable: `ssh-keygen -lf <key>`, compare by eye")
    say("    * the key-channel probe. Stage 1 REFUSES if it finds it could sign.")
    say("      -> NOT rehearsable. Probing it here would be the very act the")
    say("         N4 precondition forbids.")
    say("    * the range-report derivation over anchor..HEAD")
    say("      -> not attempted here.")

    branch = git(repo, "rev-parse", "--symbolic-full-name", "HEAD")
    say("")
    if not branch.startswith("refs/heads/"):
        say(f"  HEAD is {branch!r}, not a branch. Stage 1 will REFUSE.")
        return False
    say(f"  HEAD is on a branch ({branch}), which stage 1 requires.")
    return True


# ---------------------------------------------------------------------------
# running the stages
# ---------------------------------------------------------------------------

def ask(question: str) -> bool:
    """A yes/no the operator answers with the whole word.

    ``y`` is not accepted. The questions this asks are the ceremony's only
    human decisions, and a single keystroke is too easy to give to the wrong one.
    """
    try:
        answer = input(f"\n{question}\n  type 'yes' to continue, "
                       f"anything else to stop: ").strip()
    except (EOFError, KeyboardInterrupt):
        say("\nstopping -- nothing further was run.")
        return False
    if answer == "yes":
        return True
    say("stopping -- nothing further was run.")
    return False


def child_env(*, allow_agent: bool) -> dict:
    """The environment a stage runs in.

    ``V_*`` and ``L_*`` are removed because they are the two values readers'
    output namespaces, and an exported one used to satisfy a presence check that
    a values-file line was supposed to be the only way to satisfy. Both readers
    now unset their own; this removes them a step earlier.

    The agent socket is the stage boundary itself: stage 1 REFUSES if it finds
    it could sign, and stage 2 cannot proceed without it.
    """
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("V_", "L_"))}
    env["LC_ALL"] = "C"
    if not allow_agent:
        env.pop("SSH_AUTH_SOCK", None)
        env.pop("SSH_AGENT_PID", None)
    return env


def run_stage(cmd: list[str], *, allow_agent: bool,
              capture: bool = False) -> tuple[int, str]:
    say(f"\n  running: {' '.join(cmd)}")
    say(f"  {rule()}")
    result = subprocess.run(cmd, env=child_env(allow_agent=allow_agent),
                            check=False,
                            capture_output=capture, text=capture)
    if capture:
        sys.stdout.write(result.stdout or "")
        sys.stderr.write(result.stderr or "")
    say(f"  {rule()}")
    say(f"  exit {result.returncode}")
    return result.returncode, (result.stdout or "" if capture else "")


def packet_artifact_digest(packet: Path) -> str | None:
    for line in packet.read_text().splitlines():
        if line.startswith("artifact_sha256 "):
            return line.split(" ", 1)[1].strip()
    return None


def drive(repo: Path, values: Path, packet: Path, launcher: Path,
          candidate: str) -> int:
    package_field = values_field(values, "package")
    if package_field is None:
        stop(f"{values} has no 'package' field")
    package = Path(package_field)

    # THE ARTIFACT THAT RENDERS THE REPORT IS CHECKED BEFORE IT RUNS.
    artifact = repo / ARTIFACT_REL
    want = packet_artifact_digest(packet)
    got = sha256_file(artifact)
    if want is None:
        stop("the packet has no artifact_sha256 row")
    if want != got:
        stop(f"{ARTIFACT_REL} in the working tree is {got[:12]}, but the packet "
             f"authorizes {want[:12]}. The launcher would refuse to start it, "
             f"and this tool will not render the report from it either.")
    say(f"\n  {ARTIFACT_REL} matches the packet's artifact_sha256 ({got[:12]}),")
    say("  so the report below is rendered by bytes the packet authorizes.")

    head("Stage 1 -- the key must be unreachable")
    say("""
  Stage 1 runs the checks and writes the authorization package. It holds no
  key, and it REFUSES if it finds it could sign -- so if a passphrase prompt
  appears, DECLINE IT. The prompt is the ceremony asking whether the key is
  reachable; answering it makes the probe succeed, which is the failure case.

  This tool removes SSH_AUTH_SOCK from stage 1's environment.""")

    if package.exists():
        stop(f"the package leaf {package} already exists; stage 1 requires it "
             f"absent. Move it aside, then re-run.")
    if not ask("Run stage 1 now?"):
        return 1

    code, _ = run_stage(["/bin/sh", str(launcher), str(packet), str(values),
                         candidate], allow_agent=False)
    if code != 0:
        stop("stage 1 did not succeed. Nothing was signed and no ref moved.", code)
    if not package.exists():
        stop(f"stage 1 reported success but {package} is not there")

    head("The report -- the one judgement in this ceremony")
    say("""
  Everything else here is arithmetic. This is not. A confirmed digest over an
  unread report authorizes a state nobody looked at.""")
    code, _ = run_stage(["/bin/sh", str(artifact), "show-report", str(values)],
                        allow_agent=False)
    if code != 0:
        stop(f"show-report exited {code}, so no report was rendered. Refusing "
             f"to ask you to confirm something that was never displayed.", code)

    head("The package digest, computed twice")
    code, out = run_stage(["/bin/sh", str(artifact), "hash-package", str(values)],
                          allow_agent=False, capture=True)
    if code != 0:
        stop(f"hash-package exited {code}", code)
    ceremony_digest = ""
    for token in out.split():
        if len(token) == 64 and all(c in "0123456789abcdef" for c in token):
            ceremony_digest = token
            break
    own_digest = sha256_file(package)

    say("")
    say(f"  ceremony (hash-package)   {ceremony_digest or '(none found)'}")
    say(f"  this tool (hashlib)       {own_digest}")
    say("")
    if ceremony_digest != own_digest:
        stop("the two computations DISAGREE. That is either a package being "
             "rewritten underneath this process or a defect in one of the two "
             "programs. Either way the ceremony stops.")
    say("  They agree. Two programs, two implementations, one file -- which is")
    say("  what a single machine can honestly offer. It is NOT an out-of-band")
    say("  confirmation by a second party, and this tool does not claim it is.")
    say("")
    say("  Confirm it a third way if you want to:")
    say(f"    shasum -a 256 {package}")

    if not ask("Does the report above describe what you intend to bless?"):
        return 1

    head("Load the ceremony key now -- and not before")
    signing = values_field(values, "signing_key") or "<your key>"
    private = signing[:-4] if signing.endswith(".pub") else signing
    say("")
    say("  Until this moment the key-at-rest precondition held, and stage 1")
    say("  proved it could not sign. Loading earlier would collapse the")
    say("  boundary the two stages exist to create.")
    say("")
    say(f"    ssh-add {private}")
    if not ask("Is the key loaded?"):
        return 1

    if not os.environ.get("SSH_AUTH_SOCK"):
        say("\n  SSH_AUTH_SOCK is not set in THIS shell, so stage 2 has no agent")
        say("  to sign through. Run stage 2 from the shell where you loaded it:")
        say("")
        say(f"    /bin/sh {launcher} {packet} {values} {candidate} \\")
        say(f"        --stage2 {own_digest}")
        say("")
        say(f"  Then:  ssh-add -d {private}")
        return 1

    code, _ = run_stage(["/bin/sh", str(launcher), str(packet), str(values),
                         candidate, "--stage2", own_digest], allow_agent=True)
    if code != 0:
        say("")
        say("  Stage 2 did not succeed. PUT THE KEY AWAY BEFORE ANYTHING ELSE:")
        say(f"    ssh-add -d {private}")
        return code

    head("Done -- and NOT published")
    say("\n  The branch and the anchor moved in one transaction, locally.")
    say("\n  Two things remain, and both are yours:")
    say(f"    1.  ssh-add -d {private}")
    say(f"    2.  git push origin HEAD '+{ANCHOR_REF}:{ANCHOR_REF}'")
    say("\n  This tool does not push, ever.")
    return 0


# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only preflight for the re-anchor ceremony. Runs no "
                    "stage, writes nothing, touches no key.")
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--ceremony-dir", type=Path, required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--run", action="store_true",
                        help="perform the ceremony after the preflight clears. "
                             "Without this, the preflight reports and stops.")
    args = parser.parse_args()

    if not args.values.exists():
        stop(f"the values file {args.values} does not exist. Copy "
             f"bootstrap/reanchor-values.example outside the repository "
             f"and fill it in.")

    # THE REPOSITORY IS THE VALUES FILE'S, NOT THIS SCRIPT'S. `git -C` discovers
    # upward, so a checkout field pointing anywhere but a worktree top level
    # would bless a repository nobody named -- and a preflight measured against
    # a different tree than the ceremony operates on is worse than no preflight.
    recorded = values_field(args.values, "checkout")
    if recorded is None:
        stop(f"{args.values} has no 'checkout' field")
    repo = Path(recorded)
    if not repo.is_dir():
        stop(f"the recorded checkout {repo} is not a directory")

    here = Path(__file__).resolve().parent.parent
    if repo.resolve() != here:
        say(f"\nNOTE: the recorded checkout is {repo}, but this script lives in")
        say(f"      {here}. Everything below measures the RECORDED one, which")
        say("      is what the ceremony operates on.")

    top = git(repo, "rev-parse", "--show-toplevel")
    if Path(top).resolve() != repo.resolve():
        stop(f"the recorded checkout {repo} is not a worktree top level "
             f"(git reports {top})")

    candidate = git(repo, "rev-parse", args.candidate)
    packet = args.ceremony_dir / "authorization-packet.txt"
    launcher = args.ceremony_dir / "reanchor-launcher.sh"

    head("What this ceremony would move")
    state = compare(repo, candidate, packet)

    pair_ok = check_packet_pair(state, packet, launcher)

    rehearsal_ok = rehearse(repo, state)

    head("Where that leaves you")
    say("")
    say(f"  read-only checks   {'CLEAR' if rehearsal_ok else 'REFUSE'}")
    say(f"  packet + launcher  {'ready' if pair_ok else 'NOT ready'}")
    say("")
    if not rehearsal_ok:
        say("  Resolve the refusals above. Nothing was written and no key was")
        say("  touched.")
        return 1
    if not pair_ok:
        say("  The tree is fine; the materials are not. The packet and launcher")
        say("  are produced together by the review that reads them, and")
        say("  delivered out of band.")
        return 1

    if args.run:
        return drive(repo, args.values, packet, launcher, candidate)

    say("  Preflight only. Add --run to perform the ceremony, or run it by")
    say("  hand with the commands below.")
    say("")
    say(f"    /bin/sh {launcher} \\")
    say(f"        {packet} \\")
    say(f"        {args.values} \\")
    say(f"        {candidate}")
    say("")
    say("  Then read the report, and compute the package digest yourself.")
    say("  These two are the artifact's own subcommands, not the launcher's:")
    say("")
    say(f"    /bin/sh {repo / ARTIFACT_REL} show-report  {args.values}")
    say(f"    /bin/sh {repo / ARTIFACT_REL} hash-package {args.values}")
    say("")
    say("  THEN load the key -- not before. Stage 1 refuses if it finds it can")
    say("  sign, and that refusal is the N4 precondition doing its job.")
    say("")
    say(f"    /bin/sh {launcher} {packet} {args.values} {candidate} \\")
    say("        --stage2 <the digest you computed>")
    say("")
    say("  Then put the key away, and push. Pushing is never implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
