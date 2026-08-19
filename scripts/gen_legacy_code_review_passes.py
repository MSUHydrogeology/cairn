#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Generate the legacy **Code-review** record manifest from a named commit.

The legacy population is keyed **non-replayably**, which requires four
things this script supplies:

* **pin the legacy baseline to one named commit**, recorded in the manifest --
  so this reads the *committed tree at that commit*, never the working tree.
  Reading the working tree is what a reviewer cannot reproduce: it drifts with
  every uncommitted edit, and the exemption population would drift with it;
* enumerate ``stem -> {raw-heading digest: occurrence count}``, matching
  ``_LEGACY_PASSES``' shape so ``_is_legacy``'s k-th-occurrence rule applies
  unchanged;
* generate the candidate list **from that commit**; and
* leave the committed enumeration to be authored **independently of this
  generator** (``:867`` of the Plan-review manifest already requires that
  separation).

**It deliberately does not import the gate**, for the reason
``scripts/gen_legacy_passes.py`` states and this file inherits: the population
a gate exempts must not be defined by the gate.  The heading regexes below are
this module's own, typed from the published grammar, and must never be
rewritten to call ``_code_review_pass_lines`` or any other planner predicate.

The three admission rules, and why they are not one
---------------------------------------------------

A *record heading* is admitted when it is, at the baseline commit:

1. a **conforming Code-review pass** heading
   (``## Code review -- <reviewer> -- YYYY-MM-DD[ (round N)]``), in a plan of
   any status.  A dated reviewer heading is a real review record whoever wrote
   it, and the manifest grandfathers every pass that existed at the baseline
   commit -- including one in a plan still in flight, whose review has already
   happened and must not be invalidated by a schema that postdates it;
2. a ``## Response to code review`` heading, in a plan of any status.  The
   exact ``Answers:`` field these must now carry is *newer than every Response
   in the tree* (measured: 2 exist corpus-wide, both without it), so without
   this rule the archived plan carrying one reddens the moment the gate is
   wired, and the accepted blast radius is "no existing artifact
   violates";
3. a **non-conforming** ``## Code review...`` container heading -- the bare
   ``## Code review`` the plan template ships, or a decorated variant --
   **only when the plan's status at the baseline is already** ``archived``.

Rule 3's status restriction is the load-bearing one and it is a *safety*
boundary, not tidiness.  Measured at the baseline: 9 archived plans record
their code review under a heading that is not a conforming pass, and archived
records are immutable, so the presence obligation must be satisfiable for them
by grandfather or the gate reds permanently on records nobody may edit.  But
**every live plan also ships that same bare heading as a placeholder**.
Admitting a live plan's placeholder would let it satisfy the archive presence
obligation with no review at all -- which is precisely the defect plan
`archive-precondition-substance` closed after two plans archived on 2026-08-11
with no code review while the gate reported success.  So the container rule
reaches only artifacts that are already past the gate it would otherwise
reopen.

Two modes, and the only thing that runs either is a person typing the command
(Cairn has no CI):

    python scripts/gen_legacy_code_review_passes.py            # the literal
    python scripts/gen_legacy_code_review_passes.py --report   # the inventory
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

#: The baseline commit the manifest pins.  Recorded here **and**
#: in the planner's manifest docstring, so a reader of either sees the same
#: commit and a mismatch between them is visible rather than inferred.
BASELINE_COMMIT = "4ca44eb8d1b378a0214019270e1a2d83976c7bb0"

#: The trees whose Code-review records are enumerated.  **Plans only**: the
#: predicate this manifest feeds (`review_record_violations`) is reached only
#: for plans, so enumerating proposals would grant exemptions no gate ever
#: consults -- a manifest naming records it does not govern is a claim nobody
#: checks.
_TREES = ("dev/plans", "dev/plans/archive")

#: This generator's OWN exact-anchored Code-review pass heading.
#: Not imported from the planner -- see the module docstring.
_PASS_RE = re.compile(
    r"^## Code review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$"
)

#: Any ``## Code review`` H2 heading at all.  The set difference against
#: `_PASS_RE` is the container population rule 3 governs.
_ANY_CODE_REVIEW_RE = re.compile(r"^## Code review\b.*$")

#: A Response-to-code-review heading -- the section a pass binds to.
_RESPONSE_RE = re.compile(
    r"^## Response to code review -- (?P<author>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$"
)

#: Status line, for rule 3's `archived`-only restriction.
_STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*(?P<value>.*?)\s*$", re.M)

#: The disposition shapes this tree actually uses to answer a Code review, from
#: the real answered cases.  Used ONLY by `--report`, to resolve the digests in
#: the planner's `_LEGACY_CODE_REVIEW_DISPOSITIONS` back to readable headings:
#: that table must store digests because the planner ships as a template and the
#: neutrality gate refuses an AI-vendor name under `templates/` with no
#: exemption, while every real disposition heading carries its author's byline.
_DISPOSITION_SHAPES = ("### Sharpening", "## Response to code review",
                       "## Implementation disposition", "## Review disposition",
                       "## Archive record")

#: The verdict vocabulary, for the report's blocking-latest-pass column only.
#: The report is an inventory, never an oracle for the gate.
_CLEARING = ("ship", "accept", "accept-with-followups", "pass")
_BLOCKING = ("revise", "request changes", "block")
_VERDICT_RE = re.compile(r"^Verdict:[ \t]*(?P<value>.*?)[ \t]*$", re.M)
_EMPHASIS_RE = re.compile(r"\*\*|__")


def digest(heading: str) -> str:
    """The 16-hex-char identity of one raw heading line."""
    return hashlib.sha256(heading.encode("utf-8")).hexdigest()[:16]


def _git(args: List[str], root: Path) -> str:
    """One read-only git invocation, or a RuntimeError naming it."""
    proc = subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.strip()}")
    return proc.stdout


def artifacts(root: Path, commit: str = BASELINE_COMMIT) -> List[str]:
    """Every plan artifact path present in the tree **at** *commit*."""
    out: List[str] = []
    for rel in _TREES:
        listing = _git(
            ["ls-tree", "--name-only", f"{commit}:{rel}"], root)
        for name in listing.split("\n"):
            name = name.strip()
            if not name.endswith(".md") or name == "_template.md":
                continue
            out.append(f"{rel}/{name}")
    return sorted(out)


def read_at(root: Path, rel: str, commit: str = BASELINE_COMMIT) -> str:
    """One artifact's bytes as committed at *commit*."""
    return _git(["show", f"{commit}:{rel}"], root)


def _verdict_class(body: str) -> Optional[str]:
    """``clearing`` / ``blocking`` / None, for the report column only.

    Emphasis markers are deleted before the field is read, because the house
    form in this tree wraps the label *and* the value in one bold span
    (``**Verdict: SHIP.**``), not just the label.
    """
    for raw in _VERDICT_RE.findall(_EMPHASIS_RE.sub("", body)):
        value = re.split(r"[.,;(/]", raw, maxsplit=1)[0].strip().casefold()
        if value in _CLEARING:
            return "clearing"
        if value in _BLOCKING:
            return "blocking"
    return None


def scan(text: str, stem: str) -> Dict[str, object]:
    """Classify every Code-review record heading in one artifact's text."""
    lines = text.split("\n")
    passes: List[str] = []
    containers: List[str] = []
    responses: List[str] = []
    latest_pass: Optional[str] = None
    latest_verdict: Optional[str] = None
    h2 = [i for i, line in enumerate(lines)
          if line.startswith("## ") or line.startswith("# ")]
    for i, line in enumerate(lines):
        if _PASS_RE.match(line):
            passes.append(line)
            end = len(lines)
            for b in h2:
                if b > i:
                    end = b
                    break
            latest_pass = line
            latest_verdict = _verdict_class("\n".join(lines[i + 1:end]))
        elif _ANY_CODE_REVIEW_RE.match(line):
            containers.append(line)
        elif _RESPONSE_RE.match(line):
            responses.append(line)
    status = _STATUS_RE.search(text)
    return {
        "stem": stem,
        "status": status.group("value").strip() if status else "",
        "passes": passes,
        "containers": containers,
        "responses": responses,
        "latest_pass": latest_pass,
        "latest_verdict": latest_verdict,
    }


def admitted_headings(rec: Dict[str, object]) -> List[str]:
    """The raw headings the three admission rules grant *rec*."""
    out: List[str] = list(rec["passes"]) + list(rec["responses"])  # rules 1, 2
    if rec["status"] == "archived":                                # rule 3
        out += list(rec["containers"])
    return out


def build_manifest(root: Path,
                   commit: str = BASELINE_COMMIT) -> Dict[str, Dict[str, int]]:
    """stem -> {raw-heading digest -> occurrence count}, at *commit*."""
    manifest: Dict[str, Dict[str, int]] = {}
    for rel in artifacts(root, commit):
        stem = Path(rel).stem
        rec = scan(read_at(root, rel, commit), stem)
        counts = collections.Counter(
            digest(h) for h in admitted_headings(rec))
        if counts:
            manifest.setdefault(stem, {}).update(counts)
    return manifest


def emit_literal(manifest: Dict[str, Dict[str, int]]) -> str:
    """Render the manifest as a paste-able Python literal."""
    out = ["_LEGACY_CODE_REVIEW_RECORDS: Dict[str, Dict[str, int]] = {"]
    for stem in sorted(manifest):
        inner = manifest[stem]
        body = ", ".join(f'"{d}": {n}' for d, n in sorted(inner.items()))
        out.append(f'    "{stem}": {{{body}}},')
    out.append("}")
    return "\n".join(out)


def report(root: Path, commit: str = BASELINE_COMMIT) -> int:
    """The Code-review record inventory at *commit*, by the oracle above."""
    recs = [scan(read_at(root, rel, commit), Path(rel).stem)
            for rel in artifacts(root, commit)]
    n_pass = sum(len(r["passes"]) for r in recs)
    n_cont = sum(len(r["containers"]) for r in recs)
    n_resp = sum(len(r["responses"]) for r in recs)
    archived = [r for r in recs if r["status"] == "archived"]
    print(f"baseline commit:            {commit}")
    print(f"plan artifacts at baseline: {len(recs)}")
    print(f"conforming passes:          {n_pass}")
    print(f"container headings:         {n_cont}"
          "   <- not passes; admitted only on `archived` plans (rule 3)")
    print(f"Response headings:          {n_resp}")
    print(f"archived plans:             {len(archived)}")

    naked = [r for r in archived if not r["passes"]]
    print(f"\n-- archived plans with NO conforming pass ({len(naked)}) --")
    print("   these are why rule 3 exists; each is immutable history")
    for r in sorted(naked, key=lambda r: r["stem"]):
        print(f"   {r['stem']:45} containers={len(r['containers'])}")

    blocking = [(r, rel) for r, rel in
                zip(recs, artifacts(root, commit))
                if r["latest_verdict"] == "blocking"]
    noverdict = [r for r in recs
                 if r["passes"] and r["latest_verdict"] is None]
    print(f"\n-- plans whose LATEST pass is blocking ({len(blocking)}) --")
    print("   R3' requires the manifest to additionally name the specific")
    print("   admitted disposition heading completing each of these.  The")
    print("   planner stores both sides as digests (neutrality gate); the")
    print("   candidate headings below are how a reader resolves them.")
    for r, rel in sorted(blocking, key=lambda pair: pair[0]["stem"]):
        print(f"   {r['stem']}")
        print(f"      pass  {digest(r['latest_pass'])}  {r['latest_pass']}")
        text = read_at(root, rel, commit)
        lines = text.split("\n")
        after = lines.index(r["latest_pass"]) if r["latest_pass"] in lines else 0
        for i, line in enumerate(lines):
            if i > after and line.startswith(_DISPOSITION_SHAPES):
                print(f"      cand  {digest(line.strip())}  {line}")
    print(f"\n-- plans whose latest pass carries no verdict line "
          f"({len(noverdict)}) --")
    for r in sorted(noverdict, key=lambda r: r["stem"]):
        print(f"   status={r['status'] or '?':10} {r['stem']}")

    live_containers = [r for r in recs
                       if r["status"] != "archived" and r["containers"]]
    print(f"\n-- live plans whose container heading is REFUSED admission "
          f"({len(live_containers)}) --")
    print("   rule 3's restriction; admitting these would let a placeholder")
    print("   satisfy the archive presence obligation")
    for r in sorted(live_containers, key=lambda r: r["stem"]):
        print(f"   status={r['status'] or '?':10} {r['stem']}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="gen_legacy_code_review_passes")
    ap.add_argument("--report", action="store_true",
                    help="print the corpus inventory instead of the manifest")
    ap.add_argument("--root", type=Path, default=Path("."),
                    help="repository root (default: cwd)")
    ap.add_argument("--baseline", default=BASELINE_COMMIT,
                    help="the pinned baseline commit (default: %(default)s)")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    if args.report:
        return report(root, args.baseline)
    manifest = build_manifest(root, args.baseline)
    total = sum(sum(inner.values()) for inner in manifest.values())
    print("# generated by scripts/gen_legacy_code_review_passes.py"
          " -- do not hand-edit.")
    print(f"# baseline commit {args.baseline}")
    print(f"# {total} record(s) across {len(manifest)} stem(s).")
    print(emit_literal(manifest))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
