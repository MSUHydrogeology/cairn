#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Work-intent engine — identity / session subsystem.

Per-session agent-identity resolution: env-var + static-config sources, the
session-token digest, and the harness-session registry. stdlib-only; no
intra-package dependencies.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import List, Optional, Tuple


#: Highest-priority agent-identity override env var.  An explicit
#: escape hatch for tests / one-offs; a *global* export re-introduces
#: the shared-identity footgun (it shadows the per-session tier below),
#: so the auto-release path warns when it shadows an available session
#: var, and the doctrine flags global exports as not-recommended.
AGENT_ENV_VAR = "CAIRN_AGENT"


#: Default JSON identity-config path (stdlib JSON, no third-party dep).
#: Keys (all optional):
#:   * ``agent`` -- a static identity string (lowest-priority tier).
#:   * ``harness_session_vars`` -- a list of ``[tool_tag, env_var]``
#:     pairs **appended** to the built-in registry below, so an adopter
#:     on a different harness registers its session env var without
#:     editing this file.
DEFAULT_CONFIG_PATH = Path("~/.cairn/agent.json")


#: Built-in harness session-scoped env vars, in (tool_tag, env_var)
#: order.  Each identifies the *current session* of one agent harness;
#: the derived identity is per-session-unique, so concurrent same-tool
#: sessions get distinct identities and auto-release never cross-releases
#: between them.  Adopters extend this set via the JSON config's
#: ``harness_session_vars`` key (see :func:`effective_harness_vars`).
HARNESS_SESSION_VARS: Tuple[Tuple[str, str], ...] = (
    ("claude", "CLAUDE_CODE_SESSION_ID"),
    ("codex", "CODEX_THREAD_ID"),
    ("antigravity", "ANTIGRAVITY_TRAJECTORY_ID"),
)


def _session_digest(raw_session_id: Optional[str]) -> Optional[str]:
    """The per-session token: the 8-hex ``sha256`` slice of a raw harness
    session id, or ``None`` when the raw id is missing / empty /
    whitespace-only.

    The id is **hashed in full**, never prefix-sliced: harness session
    ids may be time-ordered (e.g. UUIDv7, whose leading bytes are a
    timestamp shared by near-simultaneous sessions), so a prefix would
    collapse exactly the concurrent same-tool sessions this identity
    model exists to separate.  Hashing the whole id is harness-neutral
    and keeps the written token safe + bounded regardless of the raw
    id's shape.

    This token is the single per-session value the rest of the system
    keys on: :func:`_session_identity` tags it (``<tool_tag>-<token>``)
    for the intent log's ``agent`` field, and :func:`resolve_session_token`
    exposes it bare for any other per-session surface that wants to link
    back to the same session (e.g. the reflections channel's
    ``<session>`` filename token).
    """
    if not raw_session_id or not raw_session_id.strip():
        return None
    return hashlib.sha256(
        raw_session_id.strip().encode("utf-8"),
    ).hexdigest()[:8]


def _session_identity(
    tool_tag: str, raw_session_id: Optional[str],
) -> Optional[str]:
    """Form a bounded, per-session agent identity from a raw session id.

    Returns ``None`` when ``raw_session_id`` is missing / empty /
    whitespace-only, so the caller falls through to the next resolution
    tier.  Otherwise returns ``<tool_tag>-<token>``, where ``<token>`` is
    the :func:`_session_digest` per-session hash.
    """
    digest = _session_digest(raw_session_id)
    if digest is None:
        return None
    return f"{tool_tag}-{digest}"


def _load_config(config_path: Optional[Path] = None) -> Optional[dict]:
    """Load the JSON identity config; return a dict or ``None``.

    ``None`` on any failure (missing file, malformed JSON, non-object
    top level) -- identity resolution then falls through.
    """
    target = config_path
    if target is None:
        home = os.environ.get("HOME")
        if not home:
            # No HOME -- try the documented default literally so an
            # explicit override path still works on platforms without
            # HOME set.
            target = DEFAULT_CONFIG_PATH.expanduser()
        else:
            target = (Path(home) / ".cairn" / "agent.json")
    target = target.expanduser()
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def effective_harness_vars(
    config: Optional[dict] = None,
) -> Tuple[Tuple[str, str], ...]:
    """Return the built-in registry plus any adopter extensions.

    Adopter extensions come from the JSON config's
    ``harness_session_vars`` key -- a list of ``[tool_tag, env_var]``
    pairs.  Malformed entries are skipped.  This is how an adopter on a
    new harness registers its session env var **without editing this
    file** (the portability contract).
    """
    extras: List[Tuple[str, str]] = []
    if config is not None:
        raw = config.get("harness_session_vars")
        if isinstance(raw, list):
            for entry in raw:
                if (
                    isinstance(entry, (list, tuple))
                    and len(entry) == 2
                    and isinstance(entry[0], str)
                    and isinstance(entry[1], str)
                    and entry[0].strip()
                    and entry[1].strip()
                ):
                    extras.append((entry[0].strip(), entry[1].strip()))
    return HARNESS_SESSION_VARS + tuple(extras)


def resolve_agent_identity(
    *,
    env_var: str = AGENT_ENV_VAR,
    config_path: Optional[Path] = None,
) -> Optional[str]:
    """Resolve the current agent identity.

    Resolution order:

    1. ``$CAIRN_AGENT`` (overrideable via ``env_var=``) -- explicit
       escape hatch.
    2. Harness session-derived identity from the **effective** registry
       (built-in + the JSON config's ``harness_session_vars`` adopter
       extensions): the first matching env var yields
       ``<tool_tag>-<8 hex of sha256(session_id)>``.
    3. The JSON config's top-level ``agent`` key (static identity).
    4. ``None``.

    Fail-soft: any resolution failure returns ``None``; the caller
    decides whether to fall back, warn, or skip.
    """
    env_val = os.environ.get(env_var)
    if env_val and env_val.strip():
        return env_val.strip()
    config = _load_config(config_path)
    for tool_tag, session_var in effective_harness_vars(config):
        derived = _session_identity(tool_tag, os.environ.get(session_var))
        if derived is not None:
            return derived
    if config is not None:
        agent = config.get("agent")
        if isinstance(agent, str) and agent.strip():
            return agent.strip()
    return None


def resolve_session_token(
    *, config_path: Optional[Path] = None,
) -> Optional[str]:
    """Resolve the bare per-session token -- the :func:`_session_digest`
    hash of the harness session id -- or ``None`` when no harness session
    var is exposed.

    This is the **token portion** of a harness-derived agent identity
    (``<tool_tag>-<token>``); :func:`resolve_agent_identity` returns the
    full identity.  Exposing the token lets a per-session surface *outside*
    the intent log reuse the same session identity: a reflections filename
    whose ``<agent>-<session>`` tail is ``<tool_tag>-<token>`` reconstructs
    the intent log's ``agent`` field exactly, so the two surfaces link.

    Resolves **only** the harness-session tier -- deliberately *not*
    ``$CAIRN_AGENT`` or the static config ``agent``.  Neither of those is
    per-session (both yield one identity shared across concurrent sessions,
    the very collision a per-session token exists to avoid), so neither
    can supply a collision-safe token; the caller falls back to a random
    token instead.
    """
    config = _load_config(config_path)
    for _tool_tag, session_var in effective_harness_vars(config):
        digest = _session_digest(os.environ.get(session_var))
        if digest is not None:
            return digest
    return None
