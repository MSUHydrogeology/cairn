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
import datetime
import hashlib
import importlib.util
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#: Review headings are evidence records; their names do not prove identity.
_REVIEW_RE = re.compile(r"^##\s+(?:Plan review|Code review|Security review)\b.*$",
                        re.M)
#: Falsification is only evidence when it carries output. A ledger that says
#: "ran the suite" and names no number is a claim, not a record.
_OUTPUT_RE = re.compile(r"\b\d[\d,]*\s+(?:passed|failed|pass|fail)\b", re.I)
_RISK_RE = re.compile(r"^\*\*(?:Risk|Assurance path|Plan review)\*\*\s*:", re.M)
_OUTCOME_RE = re.compile(r"^\*\*(?:Status|Outcome)\*\*\s*:\s*(?P<v>.+)$", re.M)

_OUTCOMES = ("archived", "pending", "superseded", "abandoned")
_BENEFIT_VERDICTS = ("worth it", "partly", "not worth it", "unknown")
_BENEFIT_LINE_RE = re.compile(
    r"^\*\*Benefit versus cost\*\*:\s*(?P<verdict>worth it|partly|not worth it|unknown)"
    r"\s+--\s*(?P<benefit>.+);\s*cost\s+(?P<cost>.+);\s*"
    r"remaining burden\s+(?P<burden>.+)\s*$", re.I)
_REVIEW_SUFFIXES = (".code-review.md", ".security-review.md",
                    ".plan-review.md", ".review.md", ".second-look.md")
_PARENT_RE = re.compile(
    r"^\*\*(?:Parent plan|Parent proposal|Parent artifact|Reviewed artifact)\*\*\s*:\s*(?P<v>.+)$",
    re.M | re.I,
)

_PULSE_SCHEMA = "cairn-pulse-artifacts/1"
_PULSE_MAX_BYTES = 8 * 1024 * 1024
_PULSE_MAX_TOTAL_BYTES = 64 * 1024 * 1024
_PULSE_MAX_FILE_BYTES = 1024 * 1024
_PULSE_MAX_FILES = 512
_PULSE_MAX_MODELS = 128
_PULSE_LABEL_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,127}\Z")
_PULSE_REVIEW_TYPES = (
    "security code review", "targeted code review return", "security review",
    "plan review", "code review", "review",
)
_PULSE_OTHER_TYPES = ("response", "decision", "implementation", "strategy")
_PULSE_REVIEW_FILE = re.compile(r"^\d{4}-\d{2}-\d{2}-code-review-", re.I)
_PULSE_MODEL_FIELD_RE = re.compile(r"^\*\*Model\*\*\s*:\s*(.*?)\s*$", re.I | re.M)
_PULSE_AUTHOR_FIELD_RE = re.compile(r"^\*\*Author\*\*\s*:\s*(.*?)\s*$", re.I | re.M)


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


def _pulse_safe_label(value: object) -> bool:
    if (not isinstance(value, str) or not value or len(value) > 2048
            or value.startswith("/") or "\\" in value or ":" in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def _pulse_sidefile(label: str) -> bool:
    name = label.rsplit("/", 1)[-1].lower()
    return (name.endswith(_REVIEW_SUFFIXES)
            or bool(_PULSE_REVIEW_FILE.match(name)))


def _pulse_sidefile_parent(label: str, text: str, labels: List[str]) -> Optional[str]:
    """Resolve only supplied labels; Markdown links are never opened or followed."""
    if not _pulse_sidefile(label):
        return None
    explicit = _PARENT_RE.findall(text)
    if explicit:
        raw_values = {value.strip().strip("`<>") for value in explicit}
        if len(raw_values) != 1:
            return None
        raw = raw_values.pop()
        if not _pulse_safe_label(raw):
            return None
        candidates = {raw}
        if not raw.endswith(".md"):
            candidates.add(raw + ".md")
        parent_dir = label.rsplit("/", 1)[0] if "/" in label else ""
        candidates.update(
            f"{parent_dir}/{item}" if parent_dir else item
            for item in tuple(candidates))
        matches = [item for item in labels if item in candidates]
        if len(matches) == 1:
            return matches[0]
        if "/" not in raw:
            basename = raw if raw.endswith(".md") else raw + ".md"
            matches = [item for item in labels if item.rsplit("/", 1)[-1] == basename]
            return matches[0] if len(matches) == 1 else None
        return None
    name = label.rsplit("/", 1)[-1]
    if _PULSE_REVIEW_FILE.match(name):
        return None
    suffix = next((item for item in _REVIEW_SUFFIXES
                   if name.lower().endswith(item)), None)
    if suffix is None:
        return None
    expected = name[:-len(suffix)] + ".md"
    matches = [item for item in labels if item.rsplit("/", 1)[-1] == expected]
    return matches[0] if len(matches) == 1 else None


def _pulse_heading(title: str):
    lowered = title.strip().casefold()
    for kind in _PULSE_REVIEW_TYPES:
        if (lowered == kind or lowered.startswith(kind + " --")
                or lowered.startswith(kind + " —") or lowered.startswith(kind + " –")):
            return "review"
    for kind in _PULSE_OTHER_TYPES:
        if (lowered == kind or lowered.startswith(kind + " ")
                or lowered.startswith(kind + " --")
                or lowered.startswith(kind + " —") or lowered.startswith(kind + " –")):
            return "other"
    return None


def _pulse_sections(text: str):
    headings = list(re.finditer(r"(?m)^##[ \t]+([^\r\n]+)\s*$", text))
    candidates = []
    for index, match in enumerate(headings):
        kind = _pulse_heading(match.group(1))
        if kind is None:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        segment = text[match.start():end]
        authored = ("--" in match.group(1) or "—" in match.group(1)
                    or "–" in match.group(1)
                    or bool(_PULSE_MODEL_FIELD_RE.search(segment))
                    or bool(_PULSE_AUTHOR_FIELD_RE.search(segment)))
        if authored:
            candidates.append({"start": match.start(), "end": end,
                               "kind": kind, "text": segment,
                               "heading": match.group(1)})
    first = candidates[0]["start"] if candidates else len(text)
    opening = text[:first]
    review_text = []
    appendix_text = []
    if candidates:
        by_start = {item["start"]: item for item in candidates}
        later_headings = [item for item in headings if item.start() >= first]
        for index, heading in enumerate(later_headings):
            end = (later_headings[index + 1].start()
                   if index + 1 < len(later_headings) else len(text))
            segment = text[heading.start():end]
            record = by_start.get(heading.start())
            if record is not None and record["kind"] == "review":
                review_text.append(segment)
            else:
                appendix_text.append(segment)
    review_passes = sum(item["kind"] == "review" for item in candidates)
    return opening, "".join(review_text), "".join(appendix_text), candidates, review_passes


def _pulse_counts(text: str) -> dict:
    return {"words": len(text.split()), "bytes": len(text.encode("utf-8"))}


def _pulse_tier(candidate: str, model_tiers: Dict[str, str]) -> str:
    matched = set()
    boundary = r"(?<![A-Za-z0-9_.+-])"
    end = r"(?![A-Za-z0-9_.+-])"
    version = r"(?:\s+v?\d+(?:[._-]\d+)*)?"
    for family, tier in model_tiers.items():
        pattern = re.compile(boundary + re.escape(family) + version + end, re.I)
        if pattern.search(candidate):
            matched.add(family.casefold())
    if len(matched) != 1:
        return "unspecified"
    family = next(iter(matched))
    return next(tier for name, tier in model_tiers.items()
                if name.casefold() == family)


def _pulse_model_observation(text: str, heading: Optional[str], model_tiers: Dict[str, str]) -> str:
    models = _PULSE_MODEL_FIELD_RE.findall(text)
    authors = _PULSE_AUTHOR_FIELD_RE.findall(text)
    if models:
        chosen = models if len({value.casefold() for value in models}) == 1 else []
    elif authors:
        chosen = authors if len({value.casefold() for value in authors}) == 1 else []
    else:
        chosen = [heading] if heading else []
    return _pulse_tier(chosen[0], model_tiers) if len(chosen) == 1 else "unspecified"


def _pulse_artifact_metrics(files: List[dict], always_loaded: List[str],
                            deliberation: List[str], model_tiers: Dict[str, str],
                            *, project_alias: str, week: str,
                            commit_label: Optional[str]) -> dict:
    """Reduce an explicit public Markdown snapshot without filesystem access."""
    by_label = {item["artifact"]: item["text"] for item in files}
    labels = list(by_label)
    cohort = [label for label in labels
              if label not in set(always_loaded) and label not in set(deliberation)]
    sidefiles = [label for label in cohort if _pulse_sidefile(label)]
    parents = [label for label in cohort if label not in sidefiles]
    attached = {label: [] for label in parents}
    orphans = []
    parent_of = {}
    for label in sidefiles:
        parent = _pulse_sidefile_parent(label, by_label[label], labels)
        if parent in attached:
            attached[parent].append(label)
            parent_of[label] = parent
        else:
            orphans.append(label)

    model_counts = {tier: 0 for tier in ("high", "medium", "low", "unspecified")}
    parent_rows = []
    combined_words = []
    combined_passes = []
    for label in sorted(parents):
        text = by_label[label]
        opening, review_text, appendix_text, records, review_passes = _pulse_sections(text)
        opening_counts = _pulse_counts(opening)
        review_counts = _pulse_counts(review_text)
        appendix_counts = _pulse_counts(appendix_text)
        model_counts[_pulse_model_observation(opening, None, model_tiers)] += 1
        for record in records:
            model_counts[_pulse_model_observation(record["text"], record["heading"],
                                                  model_tiers)] += 1
        sidefile_words = sidefile_bytes = sidefile_passes = 0
        for sidefile in sorted(attached[label]):
            side_text = by_label[sidefile]
            sidefile_words += len(side_text.split())
            sidefile_bytes += len(side_text.encode("utf-8"))
            _so, _sr, _sa, side_records, side_passes = _pulse_sections(side_text)
            sidefile_passes += side_passes or 1
            if side_records:
                for record in side_records:
                    model_counts[_pulse_model_observation(
                        record["text"], record["heading"], model_tiers)] += 1
            else:
                model_counts[_pulse_model_observation(side_text, None, model_tiers)] += 1
        total_words = (opening_counts["words"] + review_counts["words"]
                       + appendix_counts["words"] + sidefile_words)
        total_bytes = (opening_counts["bytes"] + review_counts["bytes"]
                       + appendix_counts["bytes"] + sidefile_bytes)
        total_passes = review_passes + sidefile_passes
        combined_words.append(total_words)
        combined_passes.append(total_passes)
        parent_rows.append({
            "artifact": label,
            "opening": opening_counts,
            "reviews": {"words": review_counts["words"] + sidefile_words,
                        "bytes": review_counts["bytes"] + sidefile_bytes},
            "other_appendices": appendix_counts,
            "sidefiles": sorted(attached[label]),
            "combined": {"words": total_words, "bytes": total_bytes},
            "review_passes": total_passes,
            "flags": {
                "over_4000_words": total_words > 4000,
                "over_25_kib": total_bytes > 25 * 1024,
                "over_three_review_passes": total_passes > 3,
            },
        })
    orphan_rows = []
    for label in sorted(orphans):
        text = by_label[label]
        _opening, _review, _appendix, records, passes = _pulse_sections(text)
        passes = passes or 1
        for record in records:
            model_counts[_pulse_model_observation(record["text"], record["heading"],
                                                  model_tiers)] += 1
        if not records:
            model_counts[_pulse_model_observation(text, None, model_tiers)] += 1
        counts = _pulse_counts(text)
        orphan_rows.append({"artifact": label, **counts, "review_passes": passes})

    def manifest(rows):
        chars = sum(len(by_label[label]) for label in rows)
        return {"files": len(rows), "chars": chars,
                "estimated_tokens": round(chars / 4),
                "estimator": "chars/4 proxy (estimate)",
                "completeness": "unknown"}

    median_words = statistics.median(combined_words) if combined_words else None
    median_passes = statistics.median(combined_passes) if combined_passes else None
    return {
        "source": "explicit_public_snapshot",
        "window": {"week": week, "meaning": "caller_declared_cohort_not_verified_history"},
        "coverage": {"cohort_selection": "unverified", "completeness": "unknown"},
        "project_alias": project_alias,
        "commit_label": commit_label,
        "parents": parent_rows,
        "orphans": orphan_rows,
        "orphan_labels": sorted(orphans),
        "summary": {"artifact_count": len(parent_rows),
                    "orphan_count": len(orphan_rows),
                    "median_combined_words": median_words,
                    "max_combined_words": max(combined_words) if combined_words else None,
                    "median_review_passes": median_passes,
                    "max_review_passes": max(combined_passes) if combined_passes else None},
        "model_records": {"source": "declared_record_mix_not_metered_call_mix",
                          "by_tier": model_counts},
        "always_loaded": manifest(always_loaded),
        "deliberation": {**manifest(deliberation),
                         "always_loaded": False},
    }


def _pulse_week(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-W\d{2}", value):
        return False
    try:
        year, week = int(value[:4]), int(value[-2:])
        return datetime.date.fromisocalendar(year, week, 1).strftime("%G-W%V") == value
    except (ValueError, OverflowError):
        return False


def _pulse_text_is_safe(text: str) -> bool:
    return not any((ord(char) < 32 and char not in "\t\r\n")
                   or 0x7f <= ord(char) <= 0x9f for char in text)


def _pulse_validate_bundle(data: bytes) -> dict:
    if not isinstance(data, bytes) or len(data) > _PULSE_MAX_BYTES or b"\0" in data:
        raise ValueError("bundle")

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate")
            result[key] = value
        return result

    def reject_constant(_value):
        raise ValueError("constant")

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_pairs,
                           parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError,
            TypeError, ValueError):
        raise ValueError("bundle") from None
    expected = {"schema", "project_alias", "week", "commit_label", "files",
                "always_loaded", "deliberation", "model_tiers"}
    if (type(value) is not dict or set(value) != expected
            or value["schema"] != _PULSE_SCHEMA
            or not isinstance(value["project_alias"], str)
            or not _PULSE_LABEL_RE.fullmatch(value["project_alias"])
            or not _pulse_week(value["week"])
            or (value["commit_label"] is not None and
                (not isinstance(value["commit_label"], str)
                 or not _PULSE_LABEL_RE.fullmatch(value["commit_label"])) )):
        raise ValueError("bundle")
    files = value["files"]
    if type(files) is not list or not 1 <= len(files) <= _PULSE_MAX_FILES:
        raise ValueError("bundle")
    labels = set()
    total_bytes = 0
    normalized_files = []
    for item in files:
        if type(item) is not dict or set(item) != {"artifact", "text"}:
            raise ValueError("bundle")
        label, text = item["artifact"], item["text"]
        if (not _pulse_safe_label(label) or not label.endswith(".md")
                or type(text) is not str or not _pulse_text_is_safe(text)):
            raise ValueError("bundle")
        raw = text.encode("utf-8")
        if len(raw) > _PULSE_MAX_FILE_BYTES:
            raise ValueError("bundle")
        total_bytes += len(raw)
        if total_bytes > _PULSE_MAX_BYTES or label in labels:
            raise ValueError("bundle")
        labels.add(label)
        normalized_files.append({"artifact": label, "text": text})
    categories = []
    for name in ("always_loaded", "deliberation"):
        rows = value[name]
        if type(rows) is not list or any(not _pulse_safe_label(item) for item in rows):
            raise ValueError("bundle")
        if len(rows) != len(set(rows)) or any(item not in labels for item in rows):
            raise ValueError("bundle")
        categories.append(set(rows))
    if categories[0] & categories[1] or not labels - categories[0] - categories[1]:
        raise ValueError("bundle")
    tiers = value["model_tiers"]
    if type(tiers) is not dict or len(tiers) > _PULSE_MAX_MODELS:
        raise ValueError("bundle")
    seen_families = set()
    for family, tier in tiers.items():
        if (not isinstance(family, str) or not family.strip() or len(family) > 128
                or any(ord(char) < 32 or 0x7f <= ord(char) <= 0x9f for char in family)
                or family.casefold() in seen_families
                or tier not in {"high", "medium", "low"}):
            raise ValueError("bundle")
        seen_families.add(family.casefold())
    return {**value, "files": normalized_files}


def _load_fixed_gauge_reader():
    """Load only the sibling gauge source, never a supplied target module."""
    path = Path(__file__).absolute().with_name("gauge.py")
    spec = importlib.util.spec_from_file_location("_cairn_fixed_pulse_gauge", path)
    if spec is None or spec.loader is None:
        raise ValueError("reader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pulse_input(args) -> bytes:
    if (args.root is None or not args.week or not args.project_alias or not args.artifact
            or args.sample or args.salt != "cairn-audit"):
        raise ValueError("arguments")
    if (not _PULSE_LABEL_RE.fullmatch(args.project_alias)
            or not _pulse_week(args.week)
            or (args.commit_label is not None
                and not _PULSE_LABEL_RE.fullmatch(args.commit_label))):
        raise ValueError("arguments")
    groups = [args.artifact, args.always_loaded, args.deliberation]
    labels = []
    for group in groups:
        if any(not _pulse_safe_label(label) or not label.endswith(".md") for label in group):
            raise ValueError("labels")
        labels.extend(group)
    if (not labels or len(labels) > _PULSE_MAX_FILES
            or len(labels) != len(set(labels))):
        raise ValueError("labels")
    tiers = {}
    for declaration in args.model_tier:
        if not isinstance(declaration, str) or declaration.count("=") != 1:
            raise ValueError("tiers")
        family, tier = declaration.split("=", 1)
        if (not family.strip() or len(family) > 128
                or any(ord(char) < 32 or 0x7f <= ord(char) <= 0x9f for char in family)
                or family.casefold() in {item.casefold() for item in tiers}
                or tier not in {"high", "medium", "low"}):
            raise ValueError("tiers")
        tiers[family] = tier
    if len(tiers) > _PULSE_MAX_MODELS:
        raise ValueError("tiers")

    gauge = _load_fixed_gauge_reader()
    root = Path(args.root)
    files = []
    total = 0
    identities = set()
    for label in labels:
        path = root.joinpath(*label.split("/"))
        try:
            before = gauge._check_report_path(path)
            if before.st_nlink != 1:
                raise ValueError("linked")
            raw = gauge._read_pulse_report(path, _PULSE_MAX_FILE_BYTES)
            after = gauge._check_report_path(path)
            identity = (before.st_dev, before.st_ino)
            if (identity in identities or before.st_nlink != after.st_nlink
                    or (before.st_dev, before.st_ino, before.st_size,
                        before.st_mtime_ns, before.st_ctime_ns)
                    != (after.st_dev, after.st_ino, after.st_size,
                        after.st_mtime_ns, after.st_ctime_ns)):
                raise ValueError("changed")
            identities.add(identity)
            total += len(raw)
            if total > _PULSE_MAX_BYTES:
                raise ValueError("limit")
            text = raw.decode("utf-8")
            if not _pulse_text_is_safe(text):
                raise ValueError("text")
            files.append({"artifact": label, "text": text})
        except (OSError, UnicodeError, ValueError, RecursionError):
            raise ValueError("input") from None
    bundle = {
        "schema": _PULSE_SCHEMA,
        "project_alias": args.project_alias,
        "week": args.week,
        "commit_label": args.commit_label,
        "files": files,
        "always_loaded": args.always_loaded,
        "deliberation": args.deliberation,
        "model_tiers": tiers,
    }
    _pulse_validate_bundle(json.dumps(
        bundle, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False).encode("utf-8"))
    _pulse_artifact_metrics(files, args.always_loaded, args.deliberation, tiers,
                            project_alias=args.project_alias, week=args.week,
                            commit_label=args.commit_label)
    output = (json.dumps(bundle, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    if len(output) > _PULSE_MAX_BYTES:
        raise ValueError("limit")
    return output


def _h2_sections(text: str) -> List[Tuple[str, List[str]]]:
    """Read actual H2 sections, ignoring headings in quotes and code fences."""
    sections: List[Tuple[str, List[str]]] = []
    heading: Optional[str] = None
    body: List[str] = []
    fence_char = ""
    fence_length = 0
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(">"):
            continue
        fence = re.match(r"(`{3,}|~{3,})", stripped)
        if fence:
            token = fence.group(1)
            if not fence_char:
                fence_char, fence_length = token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_length:
                fence_char, fence_length = "", 0
            continue
        if fence_char:
            continue
        if line.startswith("## "):
            if heading is not None:
                sections.append((heading, body))
            heading, body = line[3:].strip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        sections.append((heading, body))
    return sections


def _benefit_verdict(text: str) -> Tuple[str, Optional[str]]:
    """Return the final verification section's countable verdict and warning."""
    sections = [body for heading, body in _h2_sections(text)
                if re.match(r"Implementation verification\b", heading)]
    if not sections:
        return "no line", None
    lines = [line for line in sections[-1]
             if re.match(r"^\*\*Benefit versus cost\*\*\s*:", line)]
    if not lines:
        return "no line", None
    if len(lines) != 1:
        return "unknown", "duplicate current benefit-versus-cost lines"
    match = _BENEFIT_LINE_RE.fullmatch(lines[0])
    if match is None:
        return "unknown", "malformed current benefit-versus-cost line"
    return match.group("verdict").lower(), None


def _facts(path: Path, sidefiles: Optional[List[Path]] = None) -> Dict[str, object]:
    text = path.read_text(encoding="utf-8")
    sections = _h2_sections(text)
    outcome_m = _OUTCOME_RE.search(text)
    outcome = outcome_m.group("v").strip() if outcome_m else ""
    attached = sidefiles or []
    benefit, benefit_diagnostic = _benefit_verdict(text)
    return {
        "artifact": path.stem,
        "risk_answer": bool(_RISK_RE.search(text)),
        "reviews": len(_REVIEW_RE.findall(text)) + len(attached),
        "review_sidefiles": [p.name for p in attached],
        "independent_review_identity": "unknown",
        "verification": any(re.match(r"Implementation verification\b", heading)
                             for heading, _ in sections),
        "benefit_versus_cost": benefit,
        "benefit_diagnostic": benefit_diagnostic,
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
    if f["benefit_diagnostic"]:
        out.append(f"benefit-versus-cost is unknown: {f['benefit_diagnostic']}")
    if not f["falsification_output"]:
        out.append("no falsification output -- a ledger naming no numbers is a claim")
    if not f["outcome_known"]:
        out.append(f"outcome {f['outcome']!r} is not one of {_OUTCOMES}; "
                   f"use 'pending' with a revisit condition rather than "
                   f"overstating what archive proves")
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
    parser.add_argument("--pulse-input", action="store_true",
                        help="Emit a bounded public artifact snapshot for gauge --pulse.")
    parser.add_argument("--week", help="Caller-declared cohort week (YYYY-Www).")
    parser.add_argument("--project-alias", help="Explicit project label for this snapshot.")
    parser.add_argument("--artifact", action="append", default=[], metavar="PATH",
                        help="Add one explicit proposal/plan or review file.")
    parser.add_argument("--always-loaded", action="append", default=[], metavar="PATH",
                        help="Add one explicit always-loaded manifest file.")
    parser.add_argument("--deliberation", action="append", default=[], metavar="PATH",
                        help="Add one explicit deliberation file.")
    parser.add_argument("--model-tier", action="append", default=[], metavar="FAMILY=TIER",
                        help="Declare one exact model family as high, medium, or low.")
    parser.add_argument("--commit-label", help="Optional provenance label.")
    args = parser.parse_args(argv)
    if args.pulse_input:
        try:
            output = _pulse_input(args)
        except (OSError, UnicodeError, ValueError, TypeError, OverflowError,
                RecursionError):
            print("audit: pulse input incomplete: explicit public snapshot is unreadable or invalid",
                  file=sys.stderr)
            return 2
        sys.stdout.write(output.decode("utf-8"))
        return 0
    if (args.week is not None or args.project_alias is not None or args.artifact
            or args.always_loaded or args.deliberation or args.model_tier
            or args.commit_label is not None):
        parser.error("pulse-input options require --pulse-input")
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
        identity = f["independent_review_identity"]
        state = "warn" if warns else "unknown" if identity != "proven" else "ok"
        print(f"audit: [{state}] {f['artifact']} -- review-evidence={f['reviews']} "
              f"independent-review={identity} "
              f"verification={'y' if f['verification'] else 'n'} "
              f"benefit-versus-cost={json.dumps(f['benefit_versus_cost'])} "
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

    benefit_counts = {
        verdict: sum(f["benefit_versus_cost"] == verdict for f in facts)
        for verdict in _BENEFIT_VERDICTS
    }
    benefit_counts["no line"] = sum(
        f["benefit_versus_cost"] == "no line" for f in facts)
    print("audit: benefit-versus-cost totals: " + ", ".join(
        f"{verdict}={benefit_counts[verdict]}"
        for verdict in (*_BENEFIT_VERDICTS, "no line")))

    print(f"audit: {len(facts)} change(s), {flagged} with at least one warning; "
          f"{len(sidefiles)} review sidefile(s), {len(unresolved)} unresolved. "
          f"Advisory only -- nothing here blocks anything.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
