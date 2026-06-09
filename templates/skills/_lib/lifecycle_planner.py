#!/usr/bin/env python3
"""Cairn lifecycle checker/planner -- the *read-only* lifecycle aid.

This is the read-only arm of the lifecycle-mechanization program
(`doctrine/lifecycle-contract.md`).  It is a **sibling** to
`tools/lifecycle.py` (the session-routine backend), deliberately NOT an
extension of it: `lifecycle.py` is itself a complexity-debt split
candidate, and the planner composes with -- rather than deepens -- it.

What it does:

* `next <artifact>` -- report an artifact's current lifecycle **state**,
  the **legal next transitions** from it, and, for each, the
  **preconditions** the artifact does or does not yet structurally
  satisfy.
* `next <artifact> --to <state>` -- emit a **proposed** house-format
  section **scaffold** plus a **mutation manifest** (what would change)
  for the chosen transition.
* `scan` -- run the structural conformance checks over the whole local
  `dev/proposals/` + `dev/plans/` corpus and report violations.  This is
  also the **adopter-side fidelity scan** (the same checker, double duty).
* `guard` -- an **advisory** pre-commit orientation pass: summarize the
  staged set, run `claim_check` on staged `dev/` docs if it is installed,
  and remind that the shipped work-intent hook is the *blocking* layer.

The authority contract -- the load-bearing safety boundary
=========================================================

The tool may **mechanize the assembly, the gates, and the formatting**;
it must **never mechanize the judgment**.  Concretely, and enforced by
construction here:

1. **Structural attestation, not authenticity (R1).**  It attests the
   *structure and presence* of an authority-bearing artifact (a Decision
   blockquote is present and isolated; a Review section exists) and
   reports a *missing or malformed* one.  It **never certifies
   authenticity** -- a local tool has no access to the harness's chat or
   system logs, so it cannot know whether a quoted authorization was
   truly given.  The committing harness/operator remains the sole
   guarantor.
2. **Infer, validate, quote -- never invent.**  It infers structural
   state, validates the attestations committed artifacts carry, and
   quotes nothing it was not given.  A generated **review scaffold
   carries NO reviewer attribution**; a generated **Decision scaffold
   carries an empty verbatim-authorization blockquote** the operator
   must fill -- the tool never authors a disposition, a finding, or an
   authorization.
3. **A status flips only on a machine-verifiable precondition.**  When a
   transition's documentary precondition is structurally absent, the
   tool reports the **missing attestation** rather than presenting the
   transition as ready.
4. **No mutate, no commit.**  Every code path here is read-only: it
   reads files and emits text to stdout.  It never writes a file, never
   stages, never commits.  A test proves this invariant.

Read-only by construction
=========================

This module performs **no writes**.  It opens files only for reading,
runs git only with read-only subcommands, and emits every scaffold and
manifest to **stdout** -- the operator copies it into the artifact and
owns the transition.  The one consequence of a mis-run is text on the
terminal, never a changed tree.

Optional aid, not the minimum kernel (R2)
=========================================

The checker is **stdlib-only** and **vendor-neutral**, like the other
lifecycle tools.  It is an **optional aid outside the minimum mechanized
kernel** (per the stack-neutrality runtime contract): a team without a
Python runtime runs the lifecycle **manually** against
`doctrine/lifecycle-contract.md`, with no loss of the contract itself --
only of the mechanized convenience.  There is no fail-closed boot if
Python is absent and no heavy dependency.

Run:
    python tools/lifecycle_planner.py next dev/proposals/<file>.md
    python tools/lifecycle_planner.py next dev/plans/<file>.md --to executing
    python tools/lifecycle_planner.py scan
    python tools/lifecycle_planner.py guard
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# --- structured output (mirrors tools/lifecycle.py) --------------------------

_PREFIX = "lifecycle-planner:"


def _emit(message: str = "") -> None:
    """Print a normal line to stdout."""
    if message:
        print(f"{_PREFIX} {message}")
    else:
        print()


def _emit_section(title: str) -> None:
    """Print a section header so relayed output is legibly grouped."""
    print(f"\n{_PREFIX} == {title} ==")


def _warn(message: str) -> None:
    """Print a non-fatal advisory to stderr."""
    print(f"{_PREFIX} NOTE: {message}", file=sys.stderr)


class PlannerError(RuntimeError):
    """A fatal, *actionable* failure -- never a silent skip.

    Raised when a step cannot proceed and the operator must act (e.g. the
    artifact path does not exist).  `main` turns it into a non-zero exit
    with the message, not a stack trace.
    """


# --- environment resolution (read-only git, like tools/lifecycle.py) ---------


def _git_env() -> dict:
    """A noninteractive, no-pager git environment."""
    env = dict(os.environ)
    env["GIT_PAGER"] = "cat"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _repo_root(start: Optional[Path] = None) -> Path:
    """Return the git repository root containing `start` (default: cwd)."""
    cwd = str(start) if start is not None else None
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, check=True, env=_git_env(),
        )
    except FileNotFoundError as exc:
        raise PlannerError(
            "git was not found on PATH; the planner resolves the repo root via git."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise PlannerError(
            "not inside a git repository -- run the planner from within the "
            "project checkout."
        ) from exc
    return Path(out.stdout.strip())


def _git_readonly(args: List[str], root: Path) -> Optional[str]:
    """Run a **read-only** git command and return stdout, or None on failure.

    Used only by the advisory `guard` pass.  Never invoked with a mutating
    subcommand; a failure is a soft None (the guard is advisory)."""
    try:
        out = subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, text=True,
            check=False, env=_git_env(),
        )
    except OSError:
        return None
    return out.stdout if out.returncode == 0 else None


def _today() -> str:
    """Today's date as ``YYYY-MM-DD`` (local)."""
    return _dt.date.today().isoformat()


# --- the AI-vs-human identity model (R5) -------------------------------------
#
# Several preconditions turn on *who* authored a section: a review is
# authored by a reviewer (an AI agent or a human), but a Decision is a
# *human Maintainer* authority.  The model is **extensible and
# vendor-neutral, never a closed enum** -- new vendors join by
# configuration, never a code edit.  The human Maintainer is the
# **residual**: a token not on the AI-agent registry.

#: The built-in AI-agent identity registry (normalized, lower-cased first
#: token of the author name).  Extended -- never replaced -- by an
#: optional ``dev/.cairn/agent-identities.json`` (an ``ai_agents`` list),
#: so a future vendor (or a project's renamed agent) is a data edit.
_AI_AGENT_REGISTRY: frozenset = frozenset({
    "codex", "claude", "gemini", "antigravity", "cursor", "copilot",
    "qwen", "aider", "devin", "gpt", "openai", "anthropic", "agent",
})

#: Where the optional identity-registry extension lives.
_AGENT_IDENTITIES_REL = ("dev", ".cairn", "agent-identities.json")


def _load_ai_registry(root: Path) -> frozenset:
    """Return the AI-agent registry, extended by the optional config.

    The config **adds** identities; it never shrinks the built-in set, so
    a malformed or hostile config cannot reclassify a known AI agent as
    the human Maintainer.  Absent / unreadable / wrong-shape -> the
    built-in registry unchanged (fail-safe, never a crash)."""
    path = root.joinpath(*_AGENT_IDENTITIES_REL)
    if not path.is_file():
        return _AI_AGENT_REGISTRY
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _AI_AGENT_REGISTRY
    extra = data.get("ai_agents") if isinstance(data, dict) else None
    if not isinstance(extra, list):
        return _AI_AGENT_REGISTRY
    tokens = {str(t).strip().lower() for t in extra if str(t).strip()}
    return _AI_AGENT_REGISTRY | tokens


def _identity_token(name: str) -> str:
    """Normalize an author display name to its classification token.

    The first whitespace token, lower-cased (``Antigravity (External
    Reviewer)`` -> ``antigravity``; ``Claude Opus`` -> ``claude``).  This
    preserves the *real* identity rather than collapsing it to a
    closed enum."""
    first = name.strip().split()[0] if name.strip() else ""
    return re.sub(r"[^a-z0-9]", "", first.lower())


def _ai_candidate_tokens(name: str) -> List[str]:
    """All classification candidates from a display name: every whitespace
    token, lower-cased and reduced to its alphanumeric run.

    Scanning *every* token (not just the first) and matching a registry
    entry as a **prefix** keeps a versioned or punctuated agent byline from
    slipping through -- ``Claude-3.5`` -> ``claude35``, ``gpt-4o`` ->
    ``gpt4o``, ``\U0001f916 Claude`` -> ``claude`` -- the exact evasions a
    first-token exact-match would miss."""
    out: List[str] = []
    for raw in name.strip().split():
        tok = re.sub(r"[^a-z0-9]", "", raw.lower())
        if tok:
            out.append(tok)
    return out


def _is_ai_agent(name: str, registry: frozenset) -> bool:
    """True if `name` classifies as a known AI agent (else: human residual).

    A registry token matched as a **prefix** of any name token classifies
    the name as AI, so version/build suffixes (``claude35``, ``gpt4o``,
    ``claudebot``) still resolve to their agent.  The match deliberately
    **errs toward flagging**: a human whose token happens to begin with an
    agent name is over-flagged (a spurious, human-reviewable violation --
    the SAFE direction for a fidelity scan), but a versioned agent byline
    is never laundered into the human residual (the unsafe direction that
    would let an AI author a Maintainer Decision unflagged)."""
    for tok in _ai_candidate_tokens(name):
        if any(tok.startswith(agent) for agent in registry):
            return True
    return False


# --- artifact parsing --------------------------------------------------------


class Section:
    """A parsed ``##``/``###`` section header from an artifact.

    `kind` is the leading label (``Review`` / ``Response`` / ``Revised
    proposal`` / ``Decision`` / ``Plan review`` / ``Code review`` / ...);
    `name`, `role`, `date` are parsed from the ``-- <name> (<role>) --
    <date>`` tail when present; `has_blockquote` is set later for Decision
    sections; `body` is the raw text under the header."""

    def __init__(self, level: int, kind: str, name: str, role: str,
                 date: str, line_no: int) -> None:
        self.level = level
        self.kind = kind
        self.name = name
        self.role = role
        self.date = date
        self.line_no = line_no
        self.body = ""
        self.has_isolated_blockquote = False


class Artifact:
    """A parsed proposal or plan."""

    def __init__(self, path: Path, kind: str, text: str) -> None:
        self.path = path
        self.kind = kind  # "proposal" | "plan"
        self.text = text
        self.status: str = ""
        self.author: str = ""
        self.plan_review: str = ""  # "required(...)" | "not required(...)" | ""
        self.sections: List[Section] = []
        self.has_followups_migrated = False
        self.has_fidelity_signoff = False


#: ``## Review -- Antigravity (External Reviewer) -- 2026-06-08``.  The
#: name and the ``(role)`` and the date are each optional in the tail, so
#: a partially-formed header still parses (and the missing piece becomes a
#: reported gap rather than a crash).
_HEADER_RE = re.compile(
    r"^(?P<hashes>#{2,3})\s+(?P<kind>[A-Za-z][A-Za-z /-]*?)"
    r"(?:\s+--\s+(?P<name>[^()\n]+?)"
    r"(?:\s+\((?P<role>[^)\n]*)\))?"
    r"(?:\s+--\s+(?P<date>\d{4}-\d{2}-\d{2}))?"
    r"(?:\s+\(round\s+\d+\))?\s*)?$"
)

#: Section kinds whose first token we key transitions on (kept liberal so
#: ``Revised proposal``, ``Plan review``, ``Code review`` all match).
_KNOWN_KINDS = {
    "review", "response", "revised", "decision", "plan", "code",
}


def _detect_kind(path: Path) -> str:
    """``proposal`` or ``plan`` from the path; else a PlannerError."""
    parts = {p.lower() for p in path.parts}
    if "proposals" in parts:
        return "proposal"
    if "plans" in parts:
        return "plan"
    raise PlannerError(
        f"cannot tell whether {path} is a proposal or a plan -- expected it "
        "under dev/proposals/ or dev/plans/."
    )


def _parse_status(text: str) -> str:
    """Best-effort read of the ``**Status**:`` / ``Status:`` line."""
    for line in text.splitlines()[:60]:
        stripped = line.strip()
        low = stripped.lower()
        if low.startswith("**status**:") or low.startswith("status:"):
            value = stripped.split(":", 1)[1].strip().strip("*").strip()
            # Normalize "accepted -> plan" style annotations to the bare token.
            token = value.split()[0].lower() if value else ""
            return token
    return ""


def _parse_field(text: str, field: str) -> str:
    """Read a ``**<field>**:`` metadata line value (empty if absent)."""
    pat = re.compile(rf"^\s*\*?\*?{re.escape(field)}\*?\*?\s*:\s*(.+?)\s*$",
                     re.IGNORECASE)
    for line in text.splitlines()[:60]:
        m = pat.match(line)
        if m:
            return m.group(1).strip()
    return ""


def _parse_sections(text: str) -> List[Section]:
    """Parse all ``##``/``###`` headers into Section records, with bodies."""
    lines = text.splitlines()
    headers: List[Tuple[int, Section]] = []
    for i, line in enumerate(lines):
        m = _HEADER_RE.match(line)
        if not m:
            continue
        kind_raw = (m.group("kind") or "").strip()
        first = kind_raw.split()[0].lower() if kind_raw else ""
        if first not in _KNOWN_KINDS:
            continue
        sec = Section(
            level=len(m.group("hashes")),
            kind=kind_raw,
            name=(m.group("name") or "").strip(),
            role=(m.group("role") or "").strip(),
            date=(m.group("date") or "").strip(),
            line_no=i + 1,
        )
        headers.append((i, sec))
    # Attach bodies (text up to the next header of equal-or-shallower depth).
    for idx, (i, sec) in enumerate(headers):
        end = len(lines)
        for j, nxt in headers[idx + 1:]:
            if nxt.level <= sec.level:
                end = j
                break
        sec.body = "\n".join(lines[i + 1:end])
        sec.has_isolated_blockquote = _has_isolated_blockquote(sec.body)
    return [sec for _i, sec in headers]


def _has_isolated_blockquote(body: str) -> bool:
    """True if `body` contains a visually-isolated ``>`` blockquote.

    Visual isolation = at least one ``>`` line with a blank line (or the
    start of the body) immediately before it, **outside any fenced code
    block** -- a ``>`` inside ```` ``` ````/``~~~`` fences is a shell prompt,
    a diff, or a markdown example, not an authorization quote, and must not
    count.  This is a **structural** check -- presence and isolation --
    never a judgment about whether the quoted text is an authentic
    authorization (R1)."""
    in_fence = False
    prev_blank = True  # start-of-body counts as a preceding blank line
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            prev_blank = False
            continue
        if not in_fence and line.lstrip().startswith(">") and stripped != ">":
            if prev_blank:
                return True
        prev_blank = stripped == ""
    return False


def _read_artifact(path: Path) -> Artifact:
    """Read + parse a proposal/plan from disk (read-only)."""
    if not path.is_file():
        raise PlannerError(f"no such artifact: {path}")
    kind = _detect_kind(path)
    text = path.read_text(encoding="utf-8")
    art = Artifact(path, kind, text)
    art.status = _parse_status(text)
    art.author = _parse_field(text, "Author")
    art.plan_review = _parse_field(text, "Plan review")
    art.sections = _parse_sections(text)
    art.has_followups_migrated = bool(
        re.search(r"^\s*Follow-ups migrated to\s*:", text, re.MULTILINE)
    )
    art.has_fidelity_signoff = bool(
        re.search(r"Fidelity sign-off|loop-fidelity", text, re.IGNORECASE)
    )
    return art


# --- the state machines (mirror doctrine/lifecycle-contract.md) --------------

#: target-state -> human label, per artifact kind.  The *legal* set from a
#: given current status is computed in `_legal_transitions`.
_PROPOSAL_STATES = ("proposed", "reviewed", "revised", "accepted",
                    "rejected", "superseded")
_PLAN_STATES = ("open", "awaiting-plan-review", "executing", "review",
                "archived")


def _legal_transitions(art: Artifact) -> List[str]:
    """The legal next target states from the artifact's current status."""
    s = art.status
    if art.kind == "proposal":
        return {
            "": ["proposed"],
            "proposed": ["reviewed"],
            "reviewed": ["revised", "accepted", "rejected", "superseded"],
            "revised": ["reviewed", "accepted", "rejected", "superseded"],
            "accepted": [],      # archive move is a file op, not a status flip
            "rejected": [],
            "superseded": [],
        }.get(s, [])
    # plan
    requires_review = art.plan_review.lower().startswith("required")
    return {
        "": ["open"],
        "open": (["awaiting-plan-review"] if requires_review else ["executing"]),
        "awaiting-plan-review": ["executing"],
        "executing": ["review"],
        "review": ["archived"],
        "archived": [],
    }.get(s, [])


def _reviewers(art: Artifact) -> List[Section]:
    """Review-bearing sections (proposal ``Review``; plan ``Plan/Code review``)."""
    out = []
    for sec in art.sections:
        first = sec.kind.split()[0].lower() if sec.kind else ""
        if art.kind == "proposal" and first == "review":
            out.append(sec)
        elif art.kind == "plan" and (
            sec.kind.lower().startswith("plan review")
            or sec.kind.lower().startswith("code review")
        ):
            out.append(sec)
    return out


def _decisions(art: Artifact) -> List[Section]:
    return [s for s in art.sections if s.kind.split()[0:1] == ["Decision"]]


def _has_kind(art: Artifact, prefix: str) -> bool:
    return any(s.kind.lower().startswith(prefix.lower()) for s in art.sections)


# --- conformance checks (structural; used by `scan` and `next`) --------------
#
# These verify the *current* status is structurally supported by the
# documentary attestations the artifact carries -- the machine-verifiable
# half.  Each returned string is a violation; an empty list means the
# current state is structurally sound (NOT that the quotes are authentic --
# the tool never asserts authenticity, R1).


def _conformance_violations(art: Artifact, registry: frozenset) -> List[str]:
    v: List[str] = []
    s = art.status
    if art.kind == "proposal":
        if not s:
            # A proposal MUST carry a Status line. Without this floor a
            # status-less proposal short-circuits every check below and a real
            # violation (an AI-authored Decision, a missing blockquote) is
            # silently laundered -- a scan false-negative. Mirrors the
            # unconditional '**Plan review**:' floor plans carry.
            v.append(
                "no '**Status**:' line -- a proposal must carry a Status "
                "(proposed/reviewed/revised/accepted/rejected/superseded); a "
                "missing status hides every downstream conformance check."
            )
        elif s not in _PROPOSAL_STATES:
            v.append(f"unknown proposal status {s!r}")
        if s in ("reviewed", "revised", "accepted", "rejected", "superseded"):
            revs = _reviewers(art)
            if not revs:
                v.append(
                    f"status is {s!r} but no '## Review' section is present "
                    "(reviewed/revised/decided states require a prior review)."
                )
            else:
                for r in revs:
                    if art.author and r.name and _identity_token(r.name) \
                            == _identity_token(art.author):
                        v.append(
                            f"'## Review' at line {r.line_no} appears authored "
                            f"by the proposal author ({art.author!r}); a review "
                            "carries reviewer-authorship (independent reviewer)."
                        )
        if s == "revised" and not _has_kind(art, "Response"):
            v.append("status is 'revised' but no '## Response' section is present.")
        if s in ("accepted", "rejected", "superseded"):
            decs = _decisions(art)
            if not decs:
                v.append(
                    f"status is {s!r} but no '## Decision' section is present "
                    "(a terminal status requires a Maintainer Decision)."
                )
            for d in decs:
                if not d.has_isolated_blockquote:
                    v.append(
                        f"'## Decision' at line {d.line_no} carries no isolated "
                        "authorization blockquote (the verbatim authorization is "
                        "structurally absent)."
                    )
                if d.name and _is_ai_agent(d.name, registry):
                    v.append(
                        f"'## Decision' at line {d.line_no} appears authored by "
                        f"an AI agent ({d.name!r}); a Decision is a human "
                        "Maintainer authority."
                    )
    else:  # plan
        if s and s not in _PLAN_STATES:
            v.append(f"unknown plan status {s!r}")
        if not art.plan_review:
            v.append(
                "no '**Plan review**:' line (mandatory: 'required(<tier>)' or "
                "'not required(<rationale>)'; a missing line is a finding)."
            )
        requires_review = art.plan_review.lower().startswith("required")
        if s in ("executing", "review", "archived") and requires_review \
                and not _has_kind(art, "Plan review"):
            v.append(
                f"status is {s!r} and 'Plan review: required', but no "
                "'## Plan review' section has landed (review-before-implement)."
            )
        if s == "archived":
            if not _has_kind(art, "Code review"):
                v.append(
                    "status is 'archived' but no '## Code review' section is "
                    "present (a plan never archives until code review occurred)."
                )
            if not art.has_followups_migrated:
                v.append(
                    "status is 'archived' but no 'Follow-ups migrated to:' block "
                    "is present (archive precondition)."
                )
            if not art.has_fidelity_signoff:
                v.append(
                    "status is 'archived' but no loop-fidelity sign-off is "
                    "present (names the implementing commit + governing section)."
                )
    return v


# --- forward-transition recipes (preconditions a target needs) ---------------
#
# For each legal target, the *gating* preconditions: structural facts that
# must already hold for the transition to be valid, each reported met/unmet
# from the file.  When a gate is unmet the tool reports the missing
# attestation -- it never presents the transition as ready (R3 / contract
# clause 3).


def _gating_preconditions(art: Artifact, target: str,
                          registry: frozenset) -> List[Tuple[bool, str]]:
    """Return (met, description) gates for a forward transition to `target`."""
    gates: List[Tuple[bool, str]] = []
    revs = _reviewers(art)
    independent_review = any(
        r.name and (not art.author
                    or _identity_token(r.name) != _identity_token(art.author))
        for r in revs
    )
    if art.kind == "proposal":
        if target == "reviewed":
            gates.append((True,
                          "append a '## Review' (reviewer fills their own "
                          "identity; not the proposal author); append-only."))
        elif target == "revised":
            gates.append((bool(revs),
                          "a prior '## Review' section exists"))
            gates.append((True,
                          "append a '## Response' (+ optional '## Revised "
                          "proposal'); append-only."))
        elif target in ("accepted", "rejected", "superseded"):
            gates.append((independent_review,
                          "an independent '## Review' has occurred"))
            gates.append((True,
                          "append a '## Decision' (Human Maintainer) quoting the "
                          "authorization verbatim in an isolated blockquote; the "
                          "commit is Decision-only."))
            if target in ("rejected", "superseded"):
                gates.append((True,
                              "the Decision commit also moves the file to "
                              "archive/."))
    else:  # plan
        requires_review = art.plan_review.lower().startswith("required")
        if target == "awaiting-plan-review":
            gates.append((requires_review,
                          "'Plan review: required(<tier>)' (else the plan goes "
                          "straight to executing)"))
        elif target == "executing":
            if requires_review:
                gates.append((_has_kind(art, "Plan review"),
                              "a '## Plan review' section has landed (+ "
                              "Sharpening if it raised findings)"))
                gates.append((True,
                              "the plan-open and first-implementation commits "
                              "stay distinct."))
            else:
                gates.append((True,
                              "'Plan review: not required' -- execution may "
                              "combine with plan-open."))
        elif target == "review":
            gates.append((True,
                          "append a '## Code review' pass (reviewer is not the "
                          "implementing agent); append-only."))
        elif target == "archived":
            gates.append((_has_kind(art, "Code review"),
                          "a '## Code review' has occurred (archive commit is "
                          "distinct from the implementing commits)"))
            gates.append((True,
                          "every deferred follow-up has a durable home, recorded "
                          "in a 'Follow-ups migrated to:' block."))
            gates.append((True,
                          "the loop-fidelity sign-off names the implementing "
                          "commit and the governing Revised section."))
    return gates


# --- scaffolds (the proposed section + mutation manifest) --------------------
#
# Each scaffold is emitted to STDOUT.  It carries placeholders the
# operator fills; the tool NEVER fills a reviewer identity, a disposition,
# a finding, or an authorization (R2 / contract clause 2).


def _scaffold(art: Artifact, target: str, date: str) -> Tuple[str, str, List[str]]:
    """Return (status_from, status_to_or_note, [scaffold_block, manifest...])."""
    k = art.kind
    if k == "proposal":
        if target == "reviewed":
            block = (
                "## Review -- <reviewer> (<role>) -- " + date + "\n\n"
                "**Model**: <model or tier when known; 'unknown' if not>\n\n"
                "<one-paragraph orientation: who asked, what triggered the pass>\n\n"
                "**Structural-independence stance.** <author / reviewer "
                "identities; tier choice and why>\n\n"
                "**Verification done before drafting:**\n\n"
                "* <file:line reads, empirical reproducers, grep counts>\n\n"
                "**Steelman:**\n\n* <what the proposal got right>\n\n"
                "**Findings:**\n\n"
                "* **[R1] -- <title>.** <body with citations>\n\n"
                "**Covered** -- <lenses swept, each with a citation>\n"
                "**Not covered / low confidence** -- <the negative space>\n\n"
                "**Second-round recommendation**: <recommended / not, with reasons>"
            )
            manifest = [
                "Status: proposed -> reviewed",
                "append the '## Review' section above (append-only; prior "
                "sections untouched).",
                "THE REVIEWER fills their own <reviewer>/<role>/<Model> -- this "
                "tool attributes nothing.",
                "one commit for this transition.",
            ]
            return ("proposed", "reviewed", [block] + manifest)
        if target == "revised":
            block = (
                "## Response -- <author> -- " + date + "\n\n"
                "**Model**: <model or tier>\n\n"
                "For each numbered critique, one disposition token + a "
                "one-sentence rationale (proposal-Response grammar: accept / "
                "accept with modification / reject / defer):\n\n"
                "* **[R1]** <accept|accept with modification|reject|defer> -- "
                "<rationale>\n\n"
                "<If accepted critiques substantially change the proposal, add a "
                "'## Revised proposal' section and set Status: revised.>"
            )
            manifest = [
                "Status: reviewed -> revised",
                "append '## Response' (+ optional '## Revised proposal'); "
                "append-only.",
                "one commit for this transition.",
            ]
            return ("reviewed/revised", "revised", [block] + manifest)
        if target in ("accepted", "rejected", "superseded"):
            block = (
                "## Decision -- <Maintainer> -- " + date + "\n\n"
                f"**{target.capitalize()}**, <one-line disposition>.\n\n"
                "*Maintainer authorization (verbatim):*\n\n"
                "> <paste the Maintainer's verbatim authorization here -- this "
                "tool cannot certify it; the committing operator is the sole "
                "guarantor of authenticity>\n\n"
                "*Scribed by <agent> at the Maintainer's explicit instruction; "
                "this is a Decision-only commit -- Status flips and this section "
                "is appended, nothing else.*"
            )
            archive_note = (
                "this Decision commit also moves the file to archive/."
                if target in ("rejected", "superseded")
                else "an accepted proposal stays in dev/proposals/ (archive moves "
                     "later, at plan-open or the trivial-implementing commit)."
            )
            manifest = [
                f"Status: -> {target}",
                "append the '## Decision' section above; Decision-only commit "
                "(touches nothing but this section).",
                "the verbatim-authorization blockquote MUST be filled by the "
                "operator -- the tool emits an empty placeholder and never "
                "invents an authorization.",
                archive_note,
            ]
            return ("reviewed/revised", target, [block] + manifest)
    else:  # plan
        if target in ("awaiting-plan-review", "executing"):
            if target == "awaiting-plan-review":
                manifest = [
                    "Status: open -> awaiting-plan-review",
                    "no section to append yet -- the plan waits for its "
                    "'## Plan review' section to land before implementation.",
                    "(in-place status edit; plans are execution artifacts.)",
                ]
                return ("open", "awaiting-plan-review", manifest)
            block = (
                "### Plan review -- <reviewer> -- " + date + "\n\n"
                "**Model**: <model or tier>\n\n"
                "<orientation> **Findings:** ... **Coverage + second-round "
                "recommendation:** ...\n\n"
                "### Sharpening -- <author> -- " + date + "\n\n"
                "<dispositions on the findings, if any>"
            )
            manifest = [
                "Status: -> executing",
                "for a review-required plan, the '## Plan review' section (+ "
                "Sharpening if findings) must have landed first; plan-open and "
                "first-implementation commits stay distinct.",
                "review/Sharpening sections are append-only.",
            ]
            return ("open/awaiting-plan-review", "executing", [block] + manifest)
        if target == "review":
            block = (
                "## Code review -- <reviewer> -- " + date + "\n\n"
                "**Model**: <model or tier>\n\n"
                "<the reviewer is NOT the implementing agent.> Findings as a "
                "numbered list with accept(commit <sha>)/defer/wontfix "
                "dispositions. A clean final review carries a falsification "
                "ledger. End with the coverage line + recommendation."
            )
            manifest = [
                "Status: executing -> review",
                "append the '## Code review' section; append-only.",
            ]
            return ("executing", "review", [block] + manifest)
        if target == "archived":
            block = (
                "## Lasting-truth migration -- " + date + "\n\n"
                "Follow-ups migrated to:\n"
                "* <item> -> dev/PLANNING.md > <section>\n\n"
                "**Evidence shipped** / **Evidence deferred** / **Deferred "
                "evidence home**: ...\n\n"
                "**Fidelity sign-off** -- the landed implementation commit(s) "
                "<sha> match the accepted Revised section <name>."
            )
            manifest = [
                "Status: review -> archived; move the file to dev/plans/archive/.",
                "the plan-archive commit is DISTINCT from the implementing "
                "commits (proves review happened).",
                "every deferred follow-up has a durable home, named in the "
                "'Follow-ups migrated to:' block; the fidelity sign-off names the "
                "implementing commit + governing section.",
            ]
            return ("review", "archived", [block] + manifest)
    # Fallback (should be unreachable given _legal_transitions gating).
    return (art.status, target, [f"no scaffold defined for -> {target}."])


# --- subcommand: next --------------------------------------------------------


def cmd_next(args: argparse.Namespace) -> int:
    """Report state + legal transitions (+ unmet preconditions), or scaffold."""
    root = _repo_root()
    path = Path(args.artifact)
    if not path.is_absolute():
        path = (Path.cwd() / path)
    art = _read_artifact(path)
    registry = _load_ai_registry(root)
    date = args.date or _today()

    _emit_section(f"{art.kind}: {art.path.name}")
    _emit(f"current state: {art.status or '(no status line)'}")

    # Surface any current-state structural violations up front (R1 honesty).
    violations = _conformance_violations(art, registry)
    if violations:
        _emit_section("structural conformance (current state)")
        for msg in violations:
            _emit(f"VIOLATION: {msg}")
    else:
        _emit("structural conformance: current state is structurally sound.")

    legal = _legal_transitions(art)

    if not args.to:
        _emit_section("legal next transitions")
        if not legal:
            _emit("(terminal state -- no status transition; any archive move is a "
                  "file operation, not a status flip.)")
            return 0
        for target in legal:
            _emit(f"-> {target}")
            for met, desc in _gating_preconditions(art, target, registry):
                mark = "ok " if met else "MISSING"
                _emit(f"     [{mark}] {desc}")
        _emit("")
        _emit("re-run with --to <state> to emit a proposed scaffold + manifest.")
        return 0

    # --to <state>: validate legality, report gates, emit scaffold + manifest.
    target = args.to
    if target not in legal:
        _emit_section("requested transition is not legal")
        _emit(f"-> {target} is not a legal next transition from "
              f"{art.status or '(none)'}.")
        _emit(f"legal targets: {', '.join(legal) if legal else '(none)'}")
        return 1

    gates = _gating_preconditions(art, target, registry)
    unmet = [desc for met, desc in gates if not met]
    _emit_section(f"transition -> {target}: gating preconditions")
    for met, desc in gates:
        _emit(f"[{'ok ' if met else 'MISSING'}] {desc}")
    if unmet:
        _emit("")
        _emit("NOTE: one or more gating preconditions are structurally MISSING. "
              "This scaffold prepares the transition, but the tool does NOT "
              "present it as ready -- supply the missing attestation first.")

    status_from, status_to, blocks = _scaffold(art, target, date)
    _emit_section("proposed section scaffold (copy into the artifact)")
    # The scaffold block is the first element; manifest lines follow.
    print(blocks[0])
    _emit_section("mutation manifest (what would change -- you apply it)")
    for line in blocks[1:]:
        _emit(f"- {line}")
    _emit("")
    _emit("read-only: this tool emitted text only. It wrote nothing and "
          "committed nothing. You own the edit and the commit.")
    return 0


# --- subcommand: scan (also the adopter fidelity scan, R3) -------------------


def cmd_scan(args: argparse.Namespace) -> int:
    """Run structural conformance over the local dev/ corpus; report violations.

    This is the read-only checker doing double duty as the **adopter-side
    fidelity scan** (R3): the same structural checks `next` reports per
    artifact, run across `dev/proposals/` + `dev/plans/` (live files; the
    `--include-archive` flag also scans `archive/`).  Exit code is non-zero
    when any violation is found, so an adopter test wrapper can assert a
    clean corpus."""
    root = _repo_root()
    registry = _load_ai_registry(root)
    total = 0
    flagged = 0
    bases = []
    for kind_dir in ("proposals", "plans"):
        base = root / "dev" / kind_dir
        if base.is_dir():
            bases.append(base)
    _emit_section("lifecycle conformance scan")
    for base in bases:
        globs = sorted(base.glob("*.md"))
        if args.include_archive and (base / "archive").is_dir():
            globs += sorted((base / "archive").glob("*.md"))
        for path in globs:
            if path.name in ("_template.md", "README.md"):
                continue
            total += 1
            try:
                art = _read_artifact(path)
            except PlannerError as exc:
                flagged += 1
                _emit(f"{path.relative_to(root)}: UNREADABLE -- {exc}")
                continue
            violations = _conformance_violations(art, registry)
            if violations:
                flagged += 1
                rel = path.relative_to(root)
                for msg in violations:
                    _emit(f"{rel}: {msg}")
    _emit("")
    if flagged:
        _emit(f"{flagged} of {total} artifact(s) carry structural violations.")
        return 1
    _emit(f"all {total} artifact(s) structurally sound (no contract violations).")
    return 0


# --- subcommand: guard (advisory pre-commit orientation, R4) -----------------


def cmd_guard(args: argparse.Namespace) -> int:
    """Advisory pre-commit pass -- warns, never blocks (R4).

    Summarizes the staged set, runs `claim_check` on staged `dev/` docs if
    it is installed, and reminds that the **shipped work-intent hook** is
    the *blocking* layer (this tool adds no new blocking enforcement, and
    promoting `claim_check` to a fail-closed gate is a separate, gated
    decision -- out of scope here)."""
    root = _repo_root()
    _emit_section("advisory pre-commit guard (warns; never blocks)")

    staged = _git_readonly(["diff", "--cached", "--name-only"], root)
    if staged is None:
        _warn("could not read the staged set (git unavailable?) -- skipping.")
        return 0
    files = [f for f in staged.splitlines() if f.strip()]
    if not files:
        _emit("no staged changes.")
        return 0
    _emit(f"staged paths ({len(files)}):")
    for f in files:
        _emit(f"  {f}")

    # Path-scope sanity: a single mixed-purpose commit is the failure class
    # the exact-diff protocol guards against -- surface it, do not block.
    top = {f.split("/", 1)[0] for f in files}
    if len(top) > 1:
        _emit(f"NOTE: staged paths span multiple top-level areas ({', '.join(sorted(top))}); "
              "confirm this is one coherent transition, not a bundled commit.")

    # claim_check on staged dev/ docs, if the tool is installed (advisory).
    dev_docs = [f for f in files if f.startswith("dev/") and f.endswith(".md")]
    claim_check = root / "tools" / "claim_check.py"
    if dev_docs and claim_check.is_file():
        _emit("running claim_check on staged dev/ docs (advisory)...")
        proc = subprocess.run(
            [sys.executable, str(claim_check), *dev_docs],
            cwd=str(root), capture_output=True, text=True, check=False,
            env=_git_env(),
        )
        if proc.stdout.strip():
            for line in proc.stdout.splitlines():
                _emit(f"  claim_check: {line}")
        if proc.returncode != 0:
            _emit("NOTE: claim_check reported flags above (advisory -- not a "
                  "block here; resolve or mark before committing).")
    elif dev_docs:
        _warn("tools/claim_check.py not installed -- skipping the staged-doc "
              "claim check (advisory step).")

    _emit("")
    _emit("the *blocking* layer is the shipped work-intent pre-commit hook "
          "(cross-claim enforcement); this guard adds no new blocking.")
    return 0


# --- argument parsing --------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lifecycle_planner",
        description=(
            "Read-only Cairn lifecycle checker/planner. Reports artifact state, "
            "legal transitions, and unmet preconditions; emits proposed "
            "scaffolds + mutation manifests. Never mutates, never commits."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_next = sub.add_parser(
        "next",
        help="Report an artifact's state + legal transitions (+ unmet "
             "preconditions); with --to, emit a scaffold + mutation manifest.",
    )
    p_next.add_argument("artifact", help="Path to a dev/proposals/ or "
                        "dev/plans/ artifact.")
    p_next.add_argument("--to", default=None, metavar="STATE",
                        help="Target transition state to scaffold (R6). Without "
                             "it, the legal next transitions are listed.")
    p_next.add_argument("--date", default=None, metavar="YYYY-MM-DD",
                        help="Date to stamp into the scaffold (default: today).")
    p_next.set_defaults(func=cmd_next)

    p_scan = sub.add_parser(
        "scan",
        help="Structural conformance scan over the local dev/ corpus (also the "
             "adopter fidelity scan). Non-zero exit when violations are found.",
    )
    p_scan.add_argument("--include-archive", action="store_true",
                        help="Also scan dev/proposals/archive/ + "
                             "dev/plans/archive/.")
    p_scan.set_defaults(func=cmd_scan)

    p_guard = sub.add_parser(
        "guard",
        help="Advisory pre-commit orientation (staged set, claim_check on "
             "staged dev/ docs). Warns; never blocks.",
    )
    p_guard.set_defaults(func=cmd_guard)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except PlannerError as exc:
        print(f"{_PREFIX} ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
