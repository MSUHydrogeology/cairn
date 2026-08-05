#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Generate the legacy review-pass manifest, and report the pass corpus.

The review gate (`doctrine/plans.md` > "The record schema") exempts passes
that predate the schema by **membership in a fixed enumeration**, not by
comparing a heading date to a cutoff.  A date in a heading is author-written
text *inside the artifact the gate judges*, so a dated cutoff lets the gated
party buy a permanent exemption by typing a smaller number.  This script
produces that enumeration.

**It deliberately does not import the gate.**  The population a gate exempts
must not be defined by the gate: this module carries its own exact-anchored
heading regex, and must never be rewritten to call ``_pass_headings``,
``_has_kind`` or any other predicate from ``tools/lifecycle_planner.py``.  A
generator that shares the gate's parser cannot detect a defect in it -- the
same reason a fixture written by the code under test is not an oracle.

Two modes, and the only thing that runs either is a person typing the
command (Cairn has no CI):

    python scripts/gen_legacy_passes.py            # emit the manifest literal
    python scripts/gen_legacy_passes.py --report   # the corpus inventory

Identity is ``(plan stem, sha256(heading line)[:16]) -> occurrence count``:

* keyed by **stem**, not path, so archiving ``dev/plans/x.md`` ->
  ``dev/plans/archive/x.md`` does not drop a file out of the exemption;
* **counted**, so re-appending a heading byte-identical to an admitted one
  yields occurrence ``count + 1``, which is not admitted.  Without the count,
  copying an admitted heading would reopen the bypass;
* an admitted heading that is **edited** leaves the manifest and stops being
  exempt.  That is the correct direction, and append-only already forbids the
  edit.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

#: The trees whose passes are enumerated.
_TREES = (
    "dev/plans",
    "dev/plans/archive",
    "dev/proposals",
    "dev/proposals/archive",
)

#: This generator's OWN exact-anchored pass heading (the schema's S1 shape).
#: Not imported from the planner -- see the module docstring.
_PASS_RE = re.compile(
    r"^## Plan review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$"
)

#: A bare container heading: `## Plan review` with no reviewer/date tail.
#: These are *not* passes and must never satisfy the floor.
_CONTAINER_RE = re.compile(r"^## Plan review\s*$")

#: Anything else whose heading merely *starts with* "Plan review" -- the
#: prefix population a `startswith` gate wrongly accepted.
_NEAR_MISS_RE = re.compile(r"^#{2,6} Plan review\b.*$")

#: The header field the required tier is read from.
_REQUIRED_FIELD_RE = re.compile(r"^\*\*Plan review\*\*:\s*(?P<value>.*?)\s*$", re.M)

#: Status line, for the "evaluate open plans as if transitioning" report column.
_STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*(?P<value>.*?)\s*$", re.M)


def digest(heading: str) -> str:
    """The 16-hex-char identity of one heading line."""
    return hashlib.sha256(heading.encode("utf-8")).hexdigest()[:16]


def artifacts(root: Path) -> List[Path]:
    """Every tracked-looking Markdown artifact in the enumerated trees."""
    out: List[Path] = []
    for rel in _TREES:
        d = root / rel
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            if p.name == "_template.md":
                continue
            out.append(p)
    return out


def scan(path: Path) -> Dict[str, object]:
    """Classify every `Plan review*` heading in one artifact."""
    text = path.read_text(encoding="utf-8")
    passes: List[str] = []
    containers = 0
    near_misses: List[str] = []
    for line in text.split("\n"):
        if not line.startswith("#"):
            continue
        if _PASS_RE.match(line):
            passes.append(line)
        elif _CONTAINER_RE.match(line):
            containers += 1
        elif _NEAR_MISS_RE.match(line):
            near_misses.append(line)
    req = _REQUIRED_FIELD_RE.search(text)
    status = _STATUS_RE.search(text)
    return {
        "stem": path.stem,
        "is_plan": "plans" in path.parts,
        "passes": passes,
        "containers": containers,
        "near_misses": near_misses,
        "required": req.group("value") if req else "",
        "status": status.group("value") if status else "",
    }


def build_manifest(root: Path) -> Dict[str, Dict[str, int]]:
    """stem -> {heading digest -> occurrence count}."""
    manifest: Dict[str, Dict[str, int]] = {}
    for path in artifacts(root):
        rec = scan(path)
        counts = collections.Counter(digest(h) for h in rec["passes"])
        if counts:
            manifest.setdefault(rec["stem"], {}).update(counts)
    return manifest


def emit_literal(manifest: Dict[str, Dict[str, int]]) -> str:
    """Render the manifest as a paste-able Python literal."""
    lines = ["_LEGACY_PASSES: Dict[str, Dict[str, int]] = {"]
    for stem in sorted(manifest):
        inner = manifest[stem]
        body = ", ".join(f'"{d}": {n}' for d, n in sorted(inner.items()))
        lines.append(f'    "{stem}": {{{body}}},')
    lines.append("}")
    return "\n".join(lines)


def report(root: Path) -> int:
    """The corpus inventory, by the exact oracle above."""
    recs = [scan(p) for p in artifacts(root)]
    total_passes = sum(len(r["passes"]) for r in recs)
    total_containers = sum(r["containers"] for r in recs)
    total_near = sum(len(r["near_misses"]) for r in recs)

    print(f"artifacts scanned:        {len(recs)}")
    print(f"conforming passes (S1):   {total_passes}")
    print(f"bare containers:          {total_containers}"
          f"   <- not passes; must never satisfy the floor")
    print(f"near-miss headings:       {total_near}"
          f"   <- accepted by a prefix match, refused by the exact oracle")

    # Which artifacts would a tier gate apply to, and do their forms resolve?
    forms = collections.Counter()
    review_required = [r for r in recs
                       if r["required"].lower().startswith("required")]
    unresolved: List[Tuple[str, str]] = []
    for r in review_required:
        # S6 reads the FIRST PARENTHESISED GROUP ONLY; text after the closing
        # paren is rationale prose and is ignored.  Counting whole field values
        # instead reports one "form" per plan, which is a property of the prose
        # rather than of the grammar under test.
        m = re.match(r"^required\s*\(([^)]*)\)", r["required"], re.I)
        group = m.group(1) if m else ""
        forms[group] += 1
        stripped = group
        for ch in "*_`":
            stripped = stripped.replace(ch, "")
        word = re.match(r"^[A-Za-z][A-Za-z-]*", stripped.strip())
        tier = word.group(0).casefold() if word else ""
        if tier not in ("internal", "external"):
            unresolved.append((r["stem"], r["required"][:70]))
    print(f"\nreview-required artifacts: {len(review_required)}")
    print(f"distinct required(...) GROUPS (what S6 reads): {len(forms)}")
    for form, n in sorted(forms.items(), key=lambda kv: -kv[1]):
        print(f"   {n:3}  required({form})")
    print(f"\nforms that do NOT resolve to internal/external: {len(unresolved)}")
    for stem, raw in unresolved:
        print(f"   {stem}: {raw}")

    # The C.0 disclosure: who has NO conforming pass but would need one.
    print("\n-- C.0: PLANS with NO conforming S1 pass --")
    print("   (evaluated as if transitioning to `executing`, per [E4]:")
    print("    an old-format record stays green while status is `open`)")
    print("   Proposals are excluded: a proposal's `**Plan review**:` field")
    print("   DECLARES a tier for the plan it will open, so a proposal without")
    print("   a `## Plan review` pass is not a violation. Counting proposals")
    print("   here inflates the disclosure with artifacts the gate never reads.")
    naked = [r for r in review_required
             if not r["passes"] and r["is_plan"]]
    review_required = [r for r in review_required if r["is_plan"]]
    for r in sorted(naked, key=lambda r: r["stem"]):
        print(f"   status={r['status'] or '?':22} {r['stem']}"
              f"   (containers={r['containers']}, near={len(r['near_misses'])})")
    print(f"\n   would newly violate: {len(naked)} of {len(review_required)}")
    return 0


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gen_legacy_passes")
    ap.add_argument("--report", action="store_true",
                    help="print the corpus inventory instead of the manifest")
    ap.add_argument("--root", type=Path, default=Path("."),
                    help="repository root (default: cwd)")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    if args.report:
        return report(root)
    manifest = build_manifest(root)
    total = sum(sum(inner.values()) for inner in manifest.values())
    print(f"# generated by scripts/gen_legacy_passes.py -- do not hand-edit.")
    print(f"# {total} pass(es) across {len(manifest)} stem(s).")
    print(emit_literal(manifest))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
