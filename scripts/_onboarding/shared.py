#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""onboarding-activate engine -- shared defaults + identity/time helpers.

Foundational constants (the adopter-tree-relative default paths) plus the
agent-identity and UTC-timestamp helpers used when appending an activation-log
line. A leaf of the ``_onboarding/`` dependency DAG: stdlib-only, no
intra-package imports.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone


#: Default location of the tracked activation log inside the adopter's
#: deliberation tree.  Per Codex P2-5: tracked, parallel to
#: dev/intents.jsonl.  The scaffold SEEDS the file empty at install
#: time (the canonical path); the helper also carries a lazy-mkdir
#: backstop on ``append_activation_log`` for callers that bypass the
#: scaffold (existing-adopter --seed paths run against a
#: scaffold-less tree, etc.).  Per Claude External code review P3-1:
#: scaffold-seeds is the primary contract; lazy-mkdir is the
#: backstop, not the primary mechanism.
DEFAULT_LOG_REL = "dev/.cairn/onboarding-activated.jsonl"


#: Default location of PLANNING.md.
DEFAULT_PLANNING_REL = "dev/PLANNING.md"


#: Directory under the adopter tree where preset source files install.
DEFAULT_MODULES_ONBOARDING_REL = "dev/modules/onboarding"


def default_agent_identity() -> str:
    """Best-effort identifier for the agent / runner appending the
    activation log line.  Reads ``CAIRN_AGENT_ID`` env var when set;
    otherwise returns ``unknown-agent``.
    """
    return os.environ.get("CAIRN_AGENT_ID", "unknown-agent")


def utc_now_iso() -> str:
    """ISO-8601 UTC timestamp with second precision.  Matches the
    `activated-at` schema field."""
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
