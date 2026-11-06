#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The audit reporter: what a closed change can and cannot show about itself.

**Warn-only, read-only, and it blocks nothing.** Every line it prints is
advisory. A gate that refuses is a gate someone routes around; this exists to
be read at goodnight or archive, not obeyed.

**It reports evidence, not identity judgments.** A review heading or a
separate review file is visible evidence. A name alone does not prove that its
author is distinct from the change author, so independent review identity is
reported as unknown.

**The sample is picked by rule, not by the packet preparer.** Whoever assembles
a Maintainer audit has every incentive to pick the tidiest artifacts. The
sample here is a hash of committed identity -- the artifact's own name -- so it
is reproducible by anyone, and unchoosable by the person being audited.

**`pending` is a real outcome, and the point of having it.** "Landed at
archive" is implementation status. Whether a *scientific* change worked is
usually not knowable at archive time, and a vocabulary without `pending`
forces that answer to be either falsely confident or silently absent.

Usage:

    python tools/audit_report.py                 # all archived plans and review evidence
    python tools/audit_report.py --sample 3      # the rule-picked sample
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional

#: Review headings are evidence records; their names do not prove identity.
_REVIEW_RE = re.compile(r"^##\s+(?:Plan review|Code review|Security review)\b.*$",
                        re.M)
_VERIFICATION_RE = re.compile(r"^##\s+Implementation verification\b.*$", re.M)
#: Falsification is only evidence when it carries output. A ledger that says
#: "ran the suite" and names no number is a claim, not a record.
_OUTPUT_RE = re.compile(r"\b\d[\d,]*\s+(?:passed|failed|pass|fail)\b", re.I)
_RISK_RE = re.compile(r"^\*\*(?:Risk|Assurance path|Plan review)\*\*\s*:", re.M)
_OUTCOME_RE = re.compile(r"^\*\*(?:Status|Outcome)\*\*\s*:\s*(?P<v>.+)$", re.M)

_OUTCOMES = ("archived", "pending", "superseded", "abandoned")
_REVIEW_SUFFIXES = (".code-review.md", ".security-review.md",
                    ".plan-review.md", ".review.md")
_PARENT_RE = re.compile(
    r"^\*\*(?:Parent plan|Parent artifact|Reviewed artifact)\*\*\s*:\s*(?P<v>.+)$",
    re.M | re.I,
)


def _review_sidefiles(archive: Path) -> List[Path]:
    return sorted(path for path in archive.rglob("*.md")
                   if not path.name.startswith("_")
                   and path.name.lower().endswith(_REVIEW_SUFFIXES))


def _sidefile_parent(path: Path, archive: Path, plans: List[Path]) -> Optional[Path]:
    """Return a parent only for a unique explicit or same-stem file match."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    explicit = _PARENT_RE.findall(text)
    if explicit:
        raw_values = {value.strip().strip("`<>") for value in explicit}
        if len(raw_values) != 1:
            return None
        raw = raw_values.pop()
        candidate = Path(raw)
        if candidate.is_absolute() or ".." in candidate.parts:
            return None
        if not candidate.suffix:
            candidate = candidate.with_suffix(".md")
        elif candidate.suffix.lower() != ".md":
            return None
        if raw.startswith("dev/plans/archive/"):
            candidate = archive.parents[2] / candidate
        else:
            candidate = archive / candidate
        matches = [plan for plan in plans
                   if plan.resolve() == candidate.resolve()]
        return matches[0] if len(matches) == 1 else None

    suffix = next((s for s in _REVIEW_SUFFIXES
                   if path.name.lower().endswith(s)), None)
    if suffix is None:
        return None
    expected = path.name[:-len(suffix)] + ".md"
    matches = [plan for plan in plans if plan.name == expected]
    return matches[0] if len(matches) == 1 else None


def _facts(path: Path, sidefiles: Optional[List[Path]] = None) -> Dict[str, object]:
    text = path.read_text(encoding="utf-8")
    outcome_m = _OUTCOME_RE.search(text)
    outcome = outcome_m.group("v").strip() if outcome_m else ""
    attached = sidefiles or []
    return {
        "artifact": path.stem,
        "risk_answer": bool(_RISK_RE.search(text)),
        "reviews": len(_REVIEW_RE.findall(text)) + len(attached),
        "review_sidefiles": [p.name for p in attached],
        "independent_review_identity": "unknown",
        "verification": bool(_VERIFICATION_RE.search(text)),
        "falsification_output": bool(_OUTPUT_RE.search(text)),
        "outcome": outcome,
        "outcome_known": outcome.split()[0] in _OUTCOMES if outcome else False,
    }


def _warnings(f: Dict[str, object]) -> List[str]:
    out: List[str] = []
    if not f["risk_answer"]:
        out.append("no risk answer (no Risk / Assurance path / Plan review field)")
    if not f["reviews"]:
        out.append("no review evidence found")
    if not f["verification"]:
        out.append("no Implementation verification section")
    if not f["falsification_output"]:
        out.append("no falsification output -- a ledger naming no numbers is a claim")
    if not f["outcome_known"]:
        out.append(f"outcome {f['outcome']!r} is not one of {_OUTCOMES}; "
                   f"use 'pending' with a revisit condition rather than "
                   f"overstating what archive proves")
    if f.get("independent_review_identity") != "proven":
        out.append("independent reviewer identity is unknown; names are not identity proof")
    return out


def _sample(stems: List[str], k: int, salt: str) -> List[str]:
    """The documented rule: sort by sha256(salt + stem), take the first k.

    Deterministic, reproducible by anyone with the same salt, and outside the
    control of whoever assembles the packet.
    """
    return sorted(stems, key=lambda s: hashlib.sha256(
        (salt + s).encode("utf-8")).hexdigest())[:k]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="audit-report",
        description="Warn-only audit facts for closed changes. Blocks nothing.")
    parser.add_argument("--sample", type=int, default=0,
                        help="Report only the rule-picked sample of this size.")
    parser.add_argument("--salt", default="cairn-audit",
                        help="Sample salt; change it to draw a different sample.")
    parser.add_argument("--root", default=None)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent

    archive = root / "dev" / "plans" / "archive"
    if not archive.is_dir():
        print("audit: no dev/plans/archive -- nothing closed to report on.")
        return 0

    paths = sorted(p for p in archive.glob("*.md")
                   if not p.name.startswith("_")
                   and not p.name.lower().endswith(_REVIEW_SUFFIXES))
    sidefiles = _review_sidefiles(archive)
    attachments: Dict[Path, List[Path]] = {}
    unresolved: List[Path] = []
    for sidefile in sidefiles:
        parent = _sidefile_parent(sidefile, archive, paths)
        if parent is None:
            unresolved.append(sidefile)
        else:
            attachments.setdefault(parent, []).append(sidefile)
    facts = [_facts(p, attachments.get(p, [])) for p in paths]

    if args.sample:
        picked = set(_sample([f["artifact"] for f in facts], args.sample, args.salt))
        facts = [f for f in facts if f["artifact"] in picked]
        print(f"audit: sample of {len(facts)}, picked by sha256('{args.salt}' + stem) "
              f"-- reproducible, and not chosen by whoever prepared this.")

    flagged = 0
    for f in facts:
        warns = _warnings(f)
        flagged += bool(warns)
        state = "ok" if not warns else "warn"
        print(f"audit: [{state}] {f['artifact']} -- review-evidence={f['reviews']} "
              f"independent-review=unknown "
              f"verification={'y' if f['verification'] else 'n'} "
              f"falsification-output={'y' if f['falsification_output'] else 'n'} "
              f"outcome={f['outcome'] or '(none)'}")
        for w in warns:
            print(f"audit:        - {w}")

    for f in facts:
        for sidefile in f["review_sidefiles"]:
            print(f"audit: review-sidefile {sidefile} -> {f['artifact']} "
                  "(same-stem or explicit parent evidence; identity unknown)")
    for sidefile in unresolved:
        print(f"audit: review-sidefile {sidefile.relative_to(archive)} -> "
              "parent unresolved or ambiguous; not counted under a plan")

    print(f"audit: {len(facts)} change(s), {flagged} with at least one warning; "
          f"{len(sidefiles)} review sidefile(s), {len(unresolved)} unresolved. "
          f"Advisory only -- nothing here blocks anything.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
