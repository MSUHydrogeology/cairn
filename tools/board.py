#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The board: one row per active proposal and plan, plus a JSON data form.

It reads the header block (`**Field**: value` lines above the first `##`
heading) and the title line (`# ` above the first `##` heading) of each
proposal and plan, the rows of `dev/PLANNING.md` that carry one fixed wait
marker, and, under `--maintainer`, the active plan bodies for two fixed fence
words. `--json` prints what authors wrote in those header lines, the title
line and the marked roadmap rows (`schema` `"cairn-board/1"`), and derives no
value. Separate `--next` output conservatively names an advisory owner and move
from written evidence; it grants no authority and never changes `cairn-board/1`.
The
one lookup it does make is whether an active artifact's status opens with a
word from the published vocabulary (held in `tools/session.py`, so there is one
list); if not, one advisory line names it as retired or unknown. That line only
warns: every artifact is still listed, archived records are never flagged, and
`--json` is unchanged. `--maintainer` lists what authors *declared* as
waiting on the Maintainer, and names the plans that mention a fence but
declare nothing; it never decides whether a wait is over.

The artifact is authoritative; this view is derived and says so. It is
read-only and mutates nothing. A symbolic link is never read and is named in
the output.

Usage:

    python tools/board.py               # active proposals and plans
    python tools/board.py --archive     # include the archives
    python tools/board.py --maintainer  # what waits on the Maintainer
    python tools/board.py --json        # data output (schema cairn-board/1)
    python tools/board.py --next        # advisory owner and move
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import re
import stat
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#: Header fields worth a column in the terminal table, in print order. Anything
#: else an author writes in the header block is still theirs to write -- it
#: simply has no column in the plain terminal table.
_FIELDS: Tuple[str, ...] = (
    "Status",
    "Review",
    "Plan review",
    "Opened",
    "Source proposal",
    "Waiting on Maintainer",
)

_HEADER_FIELD_RE = re.compile(r"^\*\*(?P<name>[A-Za-z][A-Za-z /-]*)\*\*:\s*(?P<value>.*)$")

#: What counts as a declared wait under `--maintainer`.
_WAIT = "Waiting on Maintainer"
_FENCE_WORDS: Tuple[str, ...] = ("MAINTAINER-GATED", "MAINTAINER-ONLY")
#: `awaiting-decision`, with an optional note after the word (` -- ...`, ` (...)`).
_AWAITING_DECISION_RE = re.compile(r"^awaiting-decision(?![A-Za-z0-9_])")
#: In `dev/PLANNING.md`, the marker counts only when the line starts with it
#: (after indentation and one optional list bullet), never inside prose or
#: backticks.
_ROW_BULLET_RE = re.compile(r"^ *(?:[*-] )?")
_NEXT_NAME_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


class _NextStop(Exception):
    """A conservative reason that the advisory owner cannot be selected."""


def _next_header(text: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        match = _HEADER_FIELD_RE.match(line.strip())
        if match:
            name = match.group("name").strip()
            if name in fields:
                raise _NextStop("duplicate header authority")
            fields[name] = match.group("value").strip()
    return fields


def _next_sections(text: str):
    heading = None
    body: List[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading is not None:
                yield heading, "\n".join(body)
            heading, body = line[3:].strip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        yield heading, "\n".join(body)


def _next_plan_fence(text: str) -> None:
    """Refuse explicit human-only steps in operative plan sections."""
    # A bare declaration is ambiguous even outside a recognized section.
    in_example = False
    example_char = ""
    example_length = 0
    for line in text.splitlines():
        stripped = line.lstrip()
        fence = re.match(r"(`{3,}|~{3,})", stripped)
        if fence:
            token = fence.group(1)
            if not in_example:
                in_example, example_char, example_length = True, token[0], len(token)
            elif token[0] == example_char and len(token) >= example_length:
                in_example = False
            continue
        if not in_example and not stripped.startswith(">") and re.match(
                r"^(?:[-*]\s+)?(?:\*\*)?MAINTAINER-(?:GATED|ONLY)(?:\*\*)?\s*:",
                stripped, re.I):
            raise _NextStop("plan contains an ambiguous Maintainer-only step")
    sections = list(_next_sections(text))
    for name in ("Scope", "Sequence"):
        bodies = [body for heading, body in sections if heading == name]
        if len(bodies) > 1:
            raise _NextStop("plan operative sections are ambiguous")
        for body in bodies:
            in_fence = False
            fence_char = ""
            fence_length = 0
            for line in body.splitlines():
                stripped = line.lstrip()
                fence = re.match(r"(`{3,}|~{3,})", stripped)
                if fence:
                    token = fence.group(1)
                    if not in_fence:
                        in_fence, fence_char, fence_length = True, token[0], len(token)
                    elif token[0] == fence_char and len(token) >= fence_length:
                        in_fence = False
                    continue
                if in_fence or stripped.startswith(">"):
                    continue
                if re.search(r"\bMAINTAINER-(?:GATED|ONLY)\b", line, re.I):
                    raise _NextStop("plan contains an operative Maintainer-only step")
            if in_fence:
                raise _NextStop("plan operative sections are ambiguous")


def _next_review_state(text: str, stage: str) -> Tuple[int, int]:
    ordinary = 0
    security = 0
    for heading, body in _next_sections(text):
        if stage == "proposal" and not (
                heading.startswith("Review --")
                or heading.startswith("Security Review --")):
            continue
        if stage == "plan" and not heading.startswith("Plan review --"):
            continue
        if stage == "code" and not (
                heading.startswith("Code review --")
                or heading.startswith("Security Review --")):
            continue
        is_security = (
            "security review" in heading.lower()
            or re.search(r"^\*\*(?:Obligation|Tier)\*\*:\s*"
                         r"(?:Internal )?Security Review\b", body, re.M) is not None
        )
        verdicts = re.findall(r"^\*\*Verdict\*\*:\s*(\S+)", body, re.M)
        if len(verdicts) != 1 or verdicts[0] not in {"ACCEPT", "SHIP", "REVISE"}:
            raise _NextStop("review record is incomplete or unrecognized")
        if is_security:
            security += 1
        else:
            ordinary += 1
    if ordinary > 1 or security > 1:
        raise _NextStop("duplicate review authority")
    return ordinary, security


_NEXT_AMENDMENT_ID = re.compile(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\Z")
_NEXT_AMENDMENT_FIELDS = (
    "Prior reviewed commit", "Replacement commit",
    "Affected cells and dependencies", "Change", "Reason",
    "Required obligations",
)


def _next_amendment_fields(
        body: str, names: Tuple[str, ...] = _NEXT_AMENDMENT_FIELDS
        ) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for name in names:
        matches = re.findall(r"^\*\*" + re.escape(name)
                             + r"\*\*:\s*(.*?)\s*$", body, re.M)
        if len(matches) != 1 or not matches[0]:
            raise _NextStop("plan amendment record is incomplete or ambiguous")
        fields[name] = matches[0]
    return fields


def _next_amendment_set(value: str) -> Tuple[str, ...]:
    entries = tuple(part.strip() for part in value.split(","))
    if (not entries or any(not item for item in entries)
            or len(set(entries)) != len(entries)):
        raise _NextStop("plan amendment affected set is incomplete or ambiguous")
    return entries


def _next_amendment_obligations(value: str) -> Tuple[str, ...]:
    allowed = {
        "Internal": ("Internal",),
        "Internal Security Review": ("Internal Security Review",),
        "Internal + Internal Security Review":
            ("Internal", "Internal Security Review"),
    }
    obligations = allowed.get(value)
    if obligations is None:
        raise _NextStop("plan amendment obligations are incomplete or ambiguous")
    return obligations


def _next_plan_amendments(text: str, status: str) -> Optional[Tuple[str, str, str]]:
    """Validate the finite, text-only amendment chain before advisory selection."""
    sections = list(_next_sections(text))
    if any(heading.startswith("Plan change")
           and not re.fullmatch(r"Plan change -- .+ -- .+", heading)
           for heading, _ in sections):
        raise _NextStop("plan amendment heading is malformed")
    if any(heading.startswith("Plan amendment review")
           and not re.fullmatch(r"Plan amendment review -- .+ -- .+", heading)
           for heading, _ in sections):
        raise _NextStop("plan amendment review heading is malformed")
    changes = [(heading, body) for heading, body in sections
               if heading.startswith("Plan change -- ")]
    if not changes:
        return None

    reviews = [(heading, body) for heading, body in sections
               if heading.startswith("Plan amendment review -- ")]
    revisions = []
    seen_replacements = set()
    original_review_ids = []
    for heading, body in sections:
        if not heading.startswith("Plan review -- "):
            continue
        matches = re.findall(r"^Reviewed commit:\s*`?([^`\s]+)`?\s*$",
                             body, re.M)
        if len(matches) != 1:
            raise _NextStop("original plan review target is missing or ambiguous")
        original_review_ids.append(matches[0])
    if not original_review_ids:
        raise _NextStop("original plan review target is missing")

    for heading, body in changes:
        fields = _next_amendment_fields(body)
        prior = fields["Prior reviewed commit"]
        replacement = fields["Replacement commit"]
        if not _NEXT_AMENDMENT_ID.fullmatch(prior):
            raise _NextStop("plan amendment prior link is not a full ID")
        if not _NEXT_AMENDMENT_ID.fullmatch(replacement):
            raise _NextStop("plan amendment replacement is unresolved")
        if prior == replacement or replacement in seen_replacements:
            raise _NextStop("plan amendment links are conflicting or duplicated")
        seen_replacements.add(replacement)
        affected = _next_amendment_set(fields["Affected cells and dependencies"])
        obligations = _next_amendment_obligations(fields["Required obligations"])
        revisions.append({
            "prior": prior, "replacement": replacement,
            "affected": affected, "obligations": obligations,
            "reviews": [], "verdicts": (), "heading": heading,
        })

    baseline = revisions[0]["prior"]
    if any(not _NEXT_AMENDMENT_ID.fullmatch(value) or value != baseline
           for value in original_review_ids):
        raise _NextStop("amendment baseline cannot be established from full review records")
    for index, revision in enumerate(revisions):
        expected_prior = baseline if index == 0 else revisions[index - 1]["replacement"]
        if revision["prior"] != expected_prior:
            raise _NextStop("plan amendment chain skips or conflicts with its predecessor")

    by_pair = {(item["prior"], item["replacement"]): item for item in revisions}
    for heading, body in reviews:
        fields = _next_amendment_fields(
            body, ("Prior reviewed commit", "Replacement commit",
                   "Affected cells and dependencies"))
        pair = (fields["Prior reviewed commit"], fields["Replacement commit"])
        revision = by_pair.get(pair)
        if revision is None:
            raise _NextStop("plan amendment review has no matching revision")
        if set(_next_amendment_set(
                fields["Affected cells and dependencies"])) != set(revision["affected"]):
            raise _NextStop("plan amendment review affected set does not match")
        obligation_matches = re.findall(r"^\*\*Obligation\*\*:\s*(.*?)\s*$",
                                        body, re.M)
        verdict_matches = re.findall(r"^\*\*Verdict\*\*:\s*(.*?)\s*$",
                                     body, re.M)
        if (len(obligation_matches) != 1 or len(verdict_matches) != 1
                or obligation_matches[0] not in revision["obligations"]
                or verdict_matches[0] not in {"ACCEPT", "REVISE"}):
            raise _NextStop("plan amendment review obligation or verdict is invalid")
        revision["reviews"].append((obligation_matches[0], verdict_matches[0]))
    for revision in revisions:
        found = [obligation for obligation, _ in revision["reviews"]]
        if (len(found) != len(revision["obligations"])
                or set(found) != set(revision["obligations"])):
            raise _NextStop("plan amendment review set is incomplete or duplicated")
        revision["verdicts"] = tuple(verdict for _, verdict in revision["reviews"])

    for index in range(1, len(revisions)):
        predecessor, revision = revisions[index - 1], revisions[index]
        if "REVISE" in predecessor["verdicts"]:
            if (not set(predecessor["affected"]).issubset(revision["affected"])
                    or not set(predecessor["obligations"]).issubset(
                        revision["obligations"])):
                raise _NextStop("successor narrows unresolved amendment obligations")

    security_passes = sum(
        obligation == "Internal Security Review"
        for revision in revisions for obligation, _ in revision["reviews"])
    security_passes += sum("security review" in heading.lower()
                           for heading, _ in sections
                           if heading.startswith("Plan review -- "))
    if security_passes > 2:
        raise _NextStop("plan amendment Security Review cap is exceeded")

    dispositions: Dict[Tuple[str, str], List[str]] = {}
    for heading, body in sections:
        if not (heading.startswith("Response -- ")
                or heading.startswith("Author response -- ")
                or heading.startswith("Plan response -- ")):
            continue
        pair_fields = [bool(re.search(r"^\*\*" + re.escape(name)
                                      + r"\*\*:", body, re.M))
                       for name in ("Prior reviewed commit", "Replacement commit")]
        if any(pair_fields) and not all(pair_fields):
            raise _NextStop("amendment author response has an incomplete commit pair")
        if not all(pair_fields):
            continue
        fields = _next_amendment_fields(
            body, ("Prior reviewed commit", "Replacement commit"))
        pair = (fields["Prior reviewed commit"], fields["Replacement commit"])
        if pair not in by_pair:
            raise _NextStop("amendment author response has no matching revision")
        response_values = re.findall(r"^\*\*Disposition\*\*:\s*(.*?)\s*$",
                                     body, re.M)
        if len(response_values) != 1:
            raise _NextStop("amendment author disposition is incomplete")
        dispositions.setdefault(pair, []).append(response_values[0])
    for revision in revisions:
        pair = (revision["prior"], revision["replacement"])
        values = dispositions.get(pair, [])
        rejected = "REVISE" in revision["verdicts"]
        if rejected:
            if values:
                raise _NextStop("rejected amendment has a conflicting ready disposition")
        elif values != ["ready-to-implement"]:
            raise _NextStop("accepted amendment lacks one ready author disposition")

    latest = revisions[-1]
    if "REVISE" in latest["verdicts"]:
        if status != "revising-plan":
            raise _NextStop("latest rejected amendment cannot select implementation")
        return "plan author", "medium", "respond or revise"
    if status == "revising-plan":
        raise _NextStop("ready amendment disposition has not returned the plan to ready")
    return None


def _next_require_responses(text: str, stage: str) -> None:
    sections = list(_next_sections(text))
    prefixes = {"proposal": ("Review --", "Security Review --"),
                "plan": ("Plan review --",),
                "code": ("Code review --", "Security Review --")}[stage]
    responses = ("Response --", "Author response --", "Plan response --")
    for index, (heading, body) in enumerate(sections):
        if (heading.startswith(prefixes)
                and re.search(r"^\*\*Verdict\*\*:\s*REVISE\b", body, re.M)
                and not any(
                    h.startswith(responses) and b.strip()
                    and not (stage == "plan" and all(
                        re.search(r"^\*\*" + re.escape(field)
                                  + r"\*\*:", b, re.M)
                        for field in ("Prior reviewed commit",
                                      "Replacement commit")))
                    for h, b in sections[index + 1:])):
            raise _NextStop("review disposition requires author response")


def _next_decision(text: str) -> str:
    decisions = [body for heading, body in _next_sections(text)
                 if heading.startswith("Decision --")]
    if len(decisions) != 1:
        raise _NextStop("Decision evidence is missing or duplicated")
    tiers = re.findall(r"^\*\*Tier\*\*:\s*([A-Za-z]+)", decisions[0], re.M)
    if len(tiers) != 1 or tiers[0].lower() not in {"light", "standard", "heavy"}:
        raise _NextStop("Decision tier is missing or unrecognized")
    # Disregard only an explicitly identified alternative's outcome. Other
    # outcome words anywhere in the Decision remain evidence about this
    # Decision, or ambiguity that must stop the advisory selector.
    body = re.sub(
        r"\b(?:the|an)\s+alternative\s+(?:is|was|remains|has been)\s+"
        r"(?:not\s+)?(?:accepted|rejected|superseded|declined)\b",
        "", decisions[0], flags=re.IGNORECASE)
    words = re.findall(r"\b(?:ACCEPTED|REJECTED|SUPERSEDED|DECLINED)\b",
                       body, re.IGNORECASE)
    outcomes = []
    for line in body.splitlines():
        stripped = line.strip()
        bold = re.match(r"^\*\*(?P<marker>[^*\n]+)\*\*", stripped)
        marker = bold.group("marker").strip() if bold else stripped
        outcome = re.match(
            r"^(?P<negated>NOT\s+)?(?P<status>ACCEPTED|REJECTED|SUPERSEDED)\b"
            r"(?P<qualifier>.*)$", marker, re.IGNORECASE)
        if outcome:
            outcomes.append(outcome.groupdict())
    if (not words or any(word.upper() != "ACCEPTED" for word in words)
            or re.search(r"\bNOT\s+ACCEPTED\b", body, re.IGNORECASE)
            or len(outcomes) != 1 or outcomes[0]["negated"]
            or re.search(r"\bNOT\b", outcomes[0]["qualifier"], re.IGNORECASE)):
        raise _NextStop("Decision outcome is ambiguous or not accepted")
    return tiers[0].lower()


def _required_reviews(fields: Dict[str, str], key: str) -> Tuple[bool, bool]:
    value = fields.get(key, "")
    if not value:
        raise _NextStop("review obligation is missing")
    if key == "Review":
        pattern = r"\s*usual\s*(?:\+\s*(security\s+review)\s*)?"
    else:
        pattern = (r"\s*required\s*\(\s*internal\s*"
                   r"(?:\+\s*(internal\s+security\s+review)\s*)?\)\s*")
    match = re.fullmatch(pattern, value, re.IGNORECASE)
    if match is None:
        raise _NextStop("review obligation is unrecognized")
    return True, match.group(1) is not None


def _next_review_move(text: str, fields: Dict[str, str], key: str,
                      stage: str, *, ordinary_first: bool = True,
                      require_security: bool = False
                      ) -> Optional[Tuple[str, str, str]]:
    need_ordinary, need_security = _required_reviews(fields, key)
    if require_security and not need_security:
        raise _NextStop("heavy Decision requires a Security Review obligation")
    ordinary, security = _next_review_state(text, stage)
    if ordinary and not need_ordinary or security and not need_security:
        raise _NextStop("review evidence conflicts with its obligation")
    if ordinary_first and need_ordinary and not ordinary:
        return ("reviewer", "medium", "review")
    if need_security and not security:
        return ("Security reviewer", "high", "Security Review")
    if need_ordinary and not ordinary:
        return ("reviewer", "medium", "review")
    return None


def _trusted_intent_engine():
    """Load only the installed intent facade beside this board, never --root."""
    facade_path = _repo_root() / "tools" / "intent.py"
    engine_path = _repo_root() / "tools" / "_intent" / "__init__.py"
    if (not facade_path.exists() and not engine_path.exists()
            and not facade_path.is_symlink() and not engine_path.is_symlink()):
        return None
    for path in (facade_path, engine_path):
        try:
            if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
                raise _NextStop("installed claims reader is linked or invalid")
        except OSError as exc:
            raise _NextStop("installed claims reader is unavailable") from exc
    spec = importlib.util.spec_from_file_location(
        "_cairn_board_trusted_intent", facade_path)
    if spec is None or spec.loader is None:
        raise _NextStop("installed claims reader is unavailable")
    facade = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = facade
    try:
        spec.loader.exec_module(facade)
        return facade._load_engine()
    except Exception as exc:
        raise _NextStop("installed claims reader could not be verified") from exc
    finally:
        sys.modules.pop(spec.name, None)


def _next_claim_check(root: Path, artifact: str) -> bool:
    """Fail closed on unverifiable claims; return whether checking was used."""
    engine = _trusted_intent_engine()
    if engine is None:
        return False
    trusted_root = Path(engine._REPO_ROOT).resolve()
    if engine.shared._has_link_or_reparse(root):
        raise _NextStop("requested root contains a linked path")
    if root.resolve() != trusted_root:
        raise _NextStop("foreign root has no verified claims resolver")
    log_path, fallback = engine.shared._shared_intents_path()
    if fallback is not None:
        raise _NextStop("claims resolver fallback prevents owner selection")
    records = engine.read_log(log_path=log_path, strict=True)
    identity = engine.resolve_agent_identity()
    if not identity or identity == "unknown-agent":
        raise _NextStop("agent identity is unavailable for claims")
    claims: Dict[str, Dict[str, object]] = {}
    releases = set()
    for record in records:
        event = record["event"]
        rid = record["id"]
        if event == "claim":
            if rid in claims:
                raise _NextStop("duplicate claims authority")
            claims[str(rid)] = record
        else:
            if rid not in claims:
                raise _NextStop(
                    f"release authority is inconsistent: release id {rid!r} "
                    f"has no earlier claim")
            releases.add(rid)
    active = [claim for rid, claim in claims.items() if rid not in releases]
    relative = artifact.split(":", 1)[1]
    relative = engine.normalize_path(relative, repo_root=root)
    conflicts = []
    for claim in active:
        files = claim["files"]
        claim_paths = {
            engine.normalize_path(value, repo_root=root) for value in files
        }
        if relative in claim_paths:
            conflicts.append(claim)
    if conflicts:
        if any(claim["agent"] != identity for claim in conflicts):
            raise _NextStop("another agent holds a conflicting claim")
    return True


def _next_for_artifact(root: Path, kind: str, path: Path, text: str
                       ) -> Optional[Tuple[str, str, str, str]]:
    match = _NEXT_NAME_RE.fullmatch(path.name)
    if match is None:
        raise _NextStop("artifact name does not match the required date pattern")
    try:
        datetime.date.fromisoformat(match.group("date"))
    except ValueError as exc:
        raise _NextStop("artifact date is invalid") from exc
    fields = _next_header(text)
    status_values = [fields.get("Status", "")]
    if not status_values[0]:
        raise _NextStop("artifact status is missing")
    kernel = _session_kernel()
    status_match = kernel._STATUS_WORD_RE.match(status_values[0])
    if status_match is None:
        raise _NextStop("artifact status is unrecognized")
    status = status_match.group("word")
    if status not in kernel._STATUS_VOCABULARY[kind]:
        raise _NextStop("artifact status is unrecognized")
    if "Waiting on Maintainer" in fields:
        raise _NextStop("artifact declares a Maintainer wait")
    if kind == "plan":
        _next_plan_fence(text)
    if kind == "proposal":
        need_ordinary, need_security = _required_reviews(fields, "Review")
        ordinary, security = _next_review_state(text, "proposal")
        if ordinary > int(need_ordinary) or security > int(need_security):
            raise _NextStop("proposal review evidence conflicts")
        if status == "awaiting-review":
            if not ordinary:
                return "reviewer", "medium", "review", "proposal"
            if need_security and not security:
                return "Security reviewer", "high", "Security Review", "proposal"
            raise _NextStop("reviewed proposal has an inconsistent status")
        if status == "revising":
            if not ordinary:
                raise _NextStop("revising proposal lacks ordinary review evidence")
            if need_security and not security:
                return "Security reviewer", "high", "Security Review", "proposal"
            return "author", "medium", "respond or revise", "proposal"
        if status == "awaiting-decision":
            if not ordinary or need_security and not security:
                raise _NextStop("proposal is missing required review evidence")
            raise _NextStop("Maintainer Decision required")
        if status in {"rejected", "superseded"}:
            return None
        if status == "accepted":
            if not ordinary or need_security and not security:
                raise _NextStop("accepted proposal lacks required review evidence")
            _next_require_responses(text, "proposal")
            tier = _next_decision(text)
            if tier == "heavy" and not need_security:
                raise _NextStop(
                    "heavy Decision requires a proposal Security Review obligation")
            source_path = path.relative_to(root).as_posix()
            linked = []
            skipped: List[str] = []
            for plan_kind, plan_path, plan_text in _artifacts(root, True, skipped):
                if skipped:
                    raise _NextStop("plan join contains a linked path")
                if plan_kind != "plan":
                    continue
                plan_fields = _next_header(plan_text)
                if plan_fields.get("Source proposal") == source_path:
                    linked.append((plan_path, plan_fields.get("Status", "")))
            if len(linked) > 1:
                raise _NextStop("proposal has duplicate plan joins")
            if linked:
                return None
            if tier == "light":
                return "implementer", "low", "complete accepted scope and checks", "proposal"
            return "plan author", "medium", "triage and open the plan", "proposal"
        raise _NextStop("proposal status has no next-step rule")

    source = fields.get("Source proposal", "")
    source_parts = Path(source).parts
    if (Path(source).is_absolute() or not source.startswith("dev/proposals/")
            or ".." in source_parts):
        raise _NextStop("plan proposal join is missing or invalid")
    proposal_path = _check_source(root, source, "file", [])
    if proposal_path is None:
        raise _NextStop("plan proposal join cannot be read")
    try:
        proposal_text = proposal_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise _NextStop("plan proposal join cannot be read") from exc
    proposal_fields = _next_header(proposal_text)
    if proposal_fields.get("Status") != "accepted":
        raise _NextStop("plan source proposal is not accepted")
    tier = _next_decision(proposal_text)
    source_need_ordinary, source_need_security = _required_reviews(
        proposal_fields, "Review")
    source_ordinary, source_security = _next_review_state(
        proposal_text, "proposal")
    if (source_ordinary > int(source_need_ordinary)
            or source_security > int(source_need_security)):
        raise _NextStop("source proposal review evidence conflicts with its obligation")
    if (source_need_ordinary and not source_ordinary
            or source_need_security and not source_security):
        raise _NextStop("source proposal lacks required review evidence")
    if tier == "heavy" and not source_need_security:
        raise _NextStop(
            "heavy Decision requires a source proposal Security Review obligation")
    _next_require_responses(proposal_text, "proposal")
    plan_review_move = _next_review_move(
        text, fields, "Plan review", "plan", require_security=tier == "heavy")
    if status == "awaiting-plan-review":
        if plan_review_move is None:
            raise _NextStop("plan-review status is inconsistent")
        return (*plan_review_move, "plan")
    if (status == "revising-plan" and plan_review_move
            and plan_review_move[0] == "Security reviewer"):
        return (*plan_review_move, "plan")
    if plan_review_move is not None:
        raise _NextStop("plan is missing required plan-review evidence")
    _next_require_responses(text, "plan")
    amendment_move = _next_plan_amendments(text, status)
    if amendment_move is not None:
        return (*amendment_move, "plan")
    if status == "revising-plan":
        if not _next_review_state(text, "plan")[0]:
            raise _NextStop("revising plan lacks ordinary review evidence")
        return "plan author", "medium", "respond or revise", "plan"
    if status in {"ready-to-implement", "implementing"}:
        return "implementer", "low", "start or continue the reviewed plan", "plan"
    ordinary, security = _next_review_state(text, "code")
    need_security = tier == "heavy"
    if ordinary > 1 or security > int(need_security):
        raise _NextStop("code-review evidence conflicts with the Decision")
    if status == "awaiting-code-review":
        if not ordinary:
            return "code reviewer", "medium", "review", "plan"
        if need_security and not security:
            return "Security reviewer", "high", "Security Review", "plan"
        raise _NextStop("code-review status is inconsistent")
    if status == "revising-code":
        if not ordinary:
            raise _NextStop("revising code lacks ordinary review evidence")
        if need_security and not security:
            return "Security reviewer", "high", "Security Review", "plan"
        return "implementer", "low", "fix findings and respond", "plan"
    if status == "ready-to-archive":
        if not ordinary or need_security and not security:
            raise _NextStop("archive status lacks required code reviews")
        _next_require_responses(text, "code")
        return "implementer", "low", "complete archive preparation", "plan"
    if status == "archived":
        _next_require_responses(text, "code")
        return None
    raise _NextStop("plan status has no next-step rule")


def _next_result(root: Path) -> Dict[str, object]:
    skipped: List[str] = []
    try:
        artifacts = list(_artifacts(root, False, skipped))
    except (_BoardSourceError, OSError, UnicodeError) as exc:
        raise _NextStop("active artifact tree cannot be read") from exc
    if skipped:
        raise _NextStop("active artifact tree contains a linked path")
    for kind, path, text in artifacts:
        move = _next_for_artifact(root, kind, path, text)
        if move is None:
            continue
        role, tier, action, kind_name = move
        rel = path.relative_to(root).as_posix()
        try:
            checked = _next_claim_check(root, f"{kind_name}:{rel}")
        except _NextStop:
            raise
        except Exception as exc:
            raise _NextStop("claims ledger is unreadable or invalid") from exc
        result: Dict[str, object] = {
            "schema": "cairn-board-next/1",
            "role": role,
            "tier": tier,
            "artifact": rel,
            "move": action,
        }
        if not checked:
            result["claim_check"] = "unavailable"
        return result
    return {"schema": "cairn-board-next/1", "stop": "no eligible active artifact"}


def _render_next(result: Dict[str, object], encode) -> str:
    if "stop" in result:
        return f"NEXT: stop -- {result['stop']}"
    line = (f"NEXT ({result['role']}, {result['tier']}): "
            f"{result['artifact']} -- {result['move']}")
    if result.get("claim_check") == "unavailable":
        line += " (claim checking unavailable)"
    return encode(line)


class _BoardSourceError(Exception):
    """Raised when a board source cannot be read as a regular file or folder."""

    def __init__(self, rel: str, reason: str) -> None:
        super().__init__(f"{rel}: {reason}")
        self.rel = rel
        self.reason = reason


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _session_kernel():
    """The session kernel, which owns the terminal encoder and the status
    vocabulary, loaded from `tools/session.py`."""
    path = _repo_root() / "tools" / "session.py"
    spec = importlib.util.spec_from_file_location("_cairn_session_encoder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _encode(limit: int = 48, module=None):
    """The one terminal encoder, loaded from the session kernel.

    Values here come out of files any contributor can edit, so they are
    untrusted for display purposes. There is deliberately no local escape table
    to fall back on: a second, weaker path engages exactly when something is
    already wrong.
    """
    module = module or _session_kernel()

    def cell(value: str) -> str:
        text = module.encode_display(str(value))
        # Elision is layered outside the encoder, and the cut is taken from
        # encoded output so it cannot split a source character into a
        # half-escape that reads as something else.
        return text if len(text) <= limit else text[:limit - 1] + "\u2026"

    return cell


def _check_source(root: Path, rel: str, expect: str,
                  skipped: List[str]) -> Optional[Path]:
    """Examine each component of `rel` below `root` before following any link.

    Gives one of three answers: a symbolic link (recorded once in `skipped` by
    its highest linked component, returns `None`), a regular file or real
    folder (returns its `Path`), or anything else (raises `_BoardSourceError`,
    except for `dev/PLANNING.md` where a non-regular entry returns `None`).
    """
    parts = Path(rel).parts
    for idx in range(len(parts)):
        sub_rel = "/".join(parts[:idx + 1])
        cur = root.joinpath(*parts[:idx + 1])
        if cur.is_symlink():
            if sub_rel not in skipped:
                skipped.append(sub_rel)
            return None
        try:
            mode = cur.lstat().st_mode
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise _BoardSourceError(sub_rel, "cannot stat") from exc
        if idx < len(parts) - 1:
            if not stat.S_ISDIR(mode):
                raise _BoardSourceError(sub_rel, "not a directory")
        elif expect == "dir":
            if not stat.S_ISDIR(mode):
                raise _BoardSourceError(sub_rel, "not a directory")
        elif expect == "planning":
            if not stat.S_ISREG(mode):
                return None
        else:
            if not stat.S_ISREG(mode):
                raise _BoardSourceError(sub_rel, "not a regular file")
    return root.joinpath(*parts)


def _header_fields(text: str) -> Dict[str, str]:
    """The `**Field**: value` lines above the first `##` heading."""
    out: Dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        m = _HEADER_FIELD_RE.match(line.strip())
        if m:
            out[m.group("name").strip()] = m.group("value").strip()
    return out


def _title(text: str) -> Optional[str]:
    """The first `# ` line above the first `##` heading, or `None`."""
    for line in text.splitlines():
        if line.startswith("## "):
            break
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _artifacts(root: Path, include_archive: bool,
               skipped: Optional[List[str]] = None):
    """`(kind, path, text)` for each proposal and plan, in print order."""
    seen_skipped = skipped if skipped is not None else []
    for kind, rel in (("proposal", "dev/proposals"), ("plan", "dev/plans")):
        base = _check_source(root, rel, "dir", seen_skipped)
        if base is None:
            continue
        folders = [(rel, base)]
        if include_archive:
            arch_rel = f"{rel}/archive"
            arch = _check_source(root, arch_rel, "dir", seen_skipped)
            if arch is not None:
                folders.append((arch_rel, arch))
        for folder_rel, folder in folders:
            try:
                names = sorted(
                    entry.name for entry in folder.iterdir()
                    if entry.name.endswith(".md") and not entry.name.startswith("_")
                )
            except OSError as exc:
                raise _BoardSourceError(folder_rel, "cannot list directory") from exc
            for name in names:
                leaf_rel = f"{folder_rel}/{name}"
                path = _check_source(root, leaf_rel, "file", seen_skipped)
                if path is None:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeError) as exc:
                    raise _BoardSourceError(leaf_rel, "cannot read UTF-8 text") from exc
                yield kind, path, text


def _rows(root: Path, include_archive: bool,
          skipped: Optional[List[str]] = None) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for kind, path, text in _artifacts(root, include_archive, skipped):
        fields = _header_fields(text)
        if not fields:
            continue
        row = {"kind": kind, "artifact": path.stem,
               "archived": "yes" if path.parent.name == "archive" else ""}
        row.update({f: fields.get(f, "") for f in _FIELDS})
        rows.append(row)
    return rows


def _roadmap_waits(root: Path,
                   skipped: List[str]) -> Tuple[List[Dict[str, object]], bool]:
    """Marked wait rows in `dev/PLANNING.md` and whether the file was read."""
    planning = _check_source(root, "dev/PLANNING.md", "planning", skipped)
    if planning is None:
        return [], False
    try:
        lines = planning.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise _BoardSourceError("dev/PLANNING.md", "cannot read UTF-8 text") from exc
    waits: List[Dict[str, object]] = []
    for number, line in enumerate(lines, 1):
        m = _HEADER_FIELD_RE.match(_ROW_BULLET_RE.sub("", line, count=1).strip())
        if m and m.group("name").strip() == _WAIT:
            waits.append({"line": number, "text": m.group("value").strip()})
    return waits, True


def _waiting(root: Path) -> Dict[str, object]:
    """What authors declared as waiting on the Maintainer.

    Active artifacts only: an archived file is a record, so the archives never
    count. An artifact is listed once however many ways it qualifies, and a
    Waiting line with no text still counts as declared, so a blanked line stays
    visible. A board row qualifies only in the row form -- after leading spaces
    and one optional bullet, `**Waiting on Maintainer**: <what>` -- read by the
    same rule as a header field, so a mention in a sentence or in backticks is
    not a marker.
    """
    entries: List[Dict[str, str]] = []
    fence_only: List[str] = []
    skipped: List[str] = []
    for kind, path, text in _artifacts(root, include_archive=False, skipped=skipped):
        fields = _header_fields(text)
        declared = _WAIT in fields
        decision = bool(_AWAITING_DECISION_RE.match(fields.get("Status", "")))
        if decision or declared:
            entries.append({"kind": kind, "artifact": path.stem,
                            "reason": "awaiting-decision" if decision else "declared",
                            "text": fields.get(_WAIT, "")})
        if kind == "plan" and not declared and any(w in text for w in _FENCE_WORDS):
            fence_only.append(path.stem)
    roadmap_rows, has_planning = _roadmap_waits(root, skipped)
    planning_skipped = "dev" in skipped or "dev/PLANNING.md" in skipped
    for row in roadmap_rows:
        entries.append({"kind": "roadmap",
                        "artifact": f"dev/PLANNING.md:{row['line']}",
                        "reason": "declared",
                        "text": str(row["text"])})
    return {"entries": entries, "fence_only": fence_only,
            "has_planning": has_planning, "planning_skipped": planning_skipped,
            "skipped": skipped}


def _json_document(root: Path, include_archive: bool) -> Dict[str, object]:
    """The `cairn-board/1` JSON data document."""
    skipped: List[str] = []
    artifacts: List[Dict[str, object]] = []
    for kind, path, text in _artifacts(root, include_archive, skipped):
        fields = _header_fields(text)
        artifacts.append({
            "kind": kind,
            "id": path.stem,
            "path": path.relative_to(root).as_posix(),
            "archived": path.parent.name == "archive",
            "title": _title(text),
            "in_brief": fields.get("In brief"),
            "status": fields.get("Status"),
            "review": fields.get("Review"),
            "plan_review": fields.get("Plan review"),
            "opened": fields.get("Opened"),
            "source_proposal": fields.get("Source proposal"),
            "waiting_on_maintainer": fields.get(_WAIT),
        })
    artifacts.sort(key=lambda r: str(r["path"]))
    roadmap_waits, roadmap_read = _roadmap_waits(root, skipped)
    return {
        "schema": "cairn-board/1",
        "includes_archive": bool(include_archive),
        "artifacts": artifacts,
        "roadmap_waits": roadmap_waits,
        "roadmap_read": roadmap_read,
        "skipped_symlinks": sorted(skipped),
    }


def _render(rows: List[Dict[str, str]], encode,
            skipped: Optional[List[str]] = None, advisory: str = "") -> str:
    cols = ["kind", "artifact"] + [f for f in _FIELDS
                                   if any(r.get(f) for r in rows)] + ["archived"]
    if not any(r.get("archived") for r in rows):
        cols.remove("archived")
    lines = ["board: " + " | ".join(cols)]
    for r in rows:
        lines.append("board: " + " | ".join(encode(r.get(c, "")) for c in cols))
    lines.append(f"board: {len(rows)} row(s). Derived from header blocks; the "
                 f"artifact is authoritative.")
    if advisory:
        lines.append(f"board: {advisory}")
    for rel in skipped or ():
        lines.append(f"board: skipped (symbolic link, not read): {encode(rel)}")
    return "\n".join(lines)


def _render_waiting(found: Dict[str, object], encode) -> str:
    cols = ["kind", "artifact", "reason", "text"]
    entries = found["entries"]
    lines = ["board: " + " | ".join(cols)]
    for e in entries:
        lines.append("board: " + " | ".join(encode(e[c]) for c in cols))
    lines.append(f"board: {len(entries)} waiting on the Maintainer, as authors "
                 f"declared. The artifact or row is authoritative.")
    names = ", ".join(encode(n) for n in found["fence_only"]) or "none"
    lines.append("board: advisory -- plans that mention a fence but declare no "
                 f"wait (open each): {names}")
    lines.append("board: not listed -- pushes (git status shows them) and "
                 "anything no artifact or row declares.")
    if not found["has_planning"] and not found.get("planning_skipped"):
        lines.append("board: dev/PLANNING.md is missing -- no board rows were read.")
    for rel in found.get("skipped", ()):
        lines.append(f"board: skipped (symbolic link, not read): {encode(rel)}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="board",
        description="Proposals, plans and declared roadmap waits from Cairn's "
                    "dev/ tree. Read-only.",
        epilog=(
            "JSON form: --json prints the board as data (schema cairn-board/1).\n"
            "Field reference and worked example: Cairn's own cairn/docs/build-a-board-view.md\n"
            "(in the repository you adopted from, not in this tree)."
            "\n--next derives a separate advisory move (schema cairn-board-next/1 with --json)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--archive", action="store_true",
                        help="Include archived artifacts in the plain board "
                             "and --json. Has no effect on --maintainer.")
    parser.add_argument("--maintainer", action="store_true",
                        help="List what waits on the Maintainer instead: "
                             "proposals awaiting a decision, plans and "
                             "dev/PLANNING.md rows that declare a wait. Also "
                             "names plans that mention a fence but declare "
                             "none. Reads active artifacts only; cannot be "
                             "combined with --json.")
    parser.add_argument("--next", action="store_true",
                        help="Select one advisory owner and move from written "
                             "artifact evidence. This does not grant authority.")
    parser.add_argument("--json", action="store_true",
                        help="Print the board as JSON data (schema "
                             "cairn-board/1): header fields, title and "
                             "location of every proposal and plan, declared "
                             "roadmap waits, and skipped symbolic links. "
                             "Derives no value; cannot be combined with "
                             "--maintainer.")
    parser.add_argument("--root", default=None, help="Repository root.")
    args = parser.parse_args(argv)
    if args.json and args.maintainer:
        parser.error("--json cannot be combined with --maintainer")
    if args.next and args.maintainer:
        parser.error("--next cannot be combined with --maintainer")
    if args.next and args.archive:
        parser.error("--next always reads active artifacts; omit --archive")
    root = (Path(args.root).absolute() if args.next and args.root
            else Path(args.root).resolve() if args.root else _repo_root())
    if args.next:
        try:
            result = _next_result(root)
        except _NextStop as exc:
            result = {"schema": "cairn-board-next/1", "stop": str(exc)}
        except (OSError, ValueError, UnicodeError):
            result = {"schema": "cairn-board-next/1",
                      "stop": "written evidence is unreadable or invalid"}
        if args.json:
            print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        else:
            print(_render_next(
                result, _encode(limit=512, module=_session_kernel())))
        return 0
    if args.json:
        try:
            doc = _json_document(root, args.archive)
        except _BoardSourceError as exc:
            # ascii() is used instead of the terminal encoder so that --json loads no other file.
            print(f"board: error: cannot read {ascii(exc.rel)} ({exc.reason})",
                  file=sys.stderr)
            return 1
        print(json.dumps(doc, ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    kernel = _session_kernel()
    encode = _encode(module=kernel)
    try:
        if args.maintainer:
            print(_render_waiting(_waiting(root), encode))
            return 0
        skipped: List[str] = []
        rows = _rows(root, args.archive, skipped)
        advisory = kernel._status_advisory(
            [(r["artifact"], r["kind"], r["Status"])
             for r in rows if not r["archived"]],
            _encode(limit=200, module=kernel))
        print(_render(rows, encode, skipped, advisory))
        return 0
    except _BoardSourceError as exc:
        print(f"board: error: cannot read {encode(exc.rel)} ({exc.reason})",
              file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
