"""Framework-side guard for ``cairn/``-prefixed template tokens (fold-back #41).

Module/template docs cite Cairn's own tree as backticked ``cairn/<rel-path>``
prose tokens -- the #25 / B.1 form.  The *adopter's* ``claim_check``
deliberately skips them: there is no ``cairn/`` top-level dir in an adopter
tree to resolve against, so skipping removes adopter-side false-positives.
But that leaves the tokens **unverified on both sides** -- a ``cairn/``-prefixed
token that does not resolve in the Cairn tree passes silently in the adopter
*and* has no checker framework-side.

This is that framework-side checker, run where the Cairn tree IS present:
every ``cairn/<rel-path>`` token in a shipped Markdown template must resolve
to a real path under the Cairn root.  Placeholder tokens (carrying ``{}``,
``<>``, or ``*``) are illustrative and skipped, mirroring ``claim_check``'s
placeholder handling.

Lives in its **own** module (not ``test_doc_governance.py``, which carries
pre-existing failures) so a regression here is not lost among them.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

#: A backticked token whose first segment is ``cairn/`` (no whitespace or
#: backtick inside -- the #25/B.1 tokens are plain paths).
_CAIRN_TOKEN_RE = re.compile(r"`(cairn/[^`\s]+)`")

#: Characters that mark a token as an illustrative placeholder, not a literal
#: path (mirrors claim_check's placeholder grammar).
_PLACEHOLDER_CHARS = set("{}<>*")


pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _markdown_templates() -> list[Path]:
    return sorted(TEMPLATES_ROOT.rglob("*.md"))


def _cairn_tokens(text: str):
    for m in _CAIRN_TOKEN_RE.finditer(text):
        tok = m.group(1)
        if any(c in _PLACEHOLDER_CHARS for c in tok):
            continue  # illustrative placeholder (e.g. cairn/.../{preset}.md)
        yield tok


def _resolves(token: str) -> bool:
    """A ``cairn/<rel-path>`` token resolves when ``<cairn-root>/<rel-path>``
    exists (trailing slash on a dir token is fine -- Path normalizes it)."""
    rel = token[len("cairn/"):]
    return (CAIRN_ROOT / rel).exists()


def test_every_cairn_prefixed_template_token_resolves():
    unresolved: list[str] = []
    for f in _markdown_templates():
        for tok in _cairn_tokens(f.read_text(encoding="utf-8")):
            if not _resolves(tok):
                unresolved.append(f"{f.relative_to(CAIRN_ROOT)}: `{tok}`")
    assert not unresolved, (
        "cairn/-prefixed template token(s) do not resolve in the Cairn "
        "tree:\n" + "\n".join(unresolved)
    )


def test_guard_catches_a_broken_token():
    # The guard logic itself must reject a deliberately-broken token --
    # otherwise the test above could pass vacuously.
    bad = "see `cairn/does-not-exist-xyz.md` for details"
    toks = list(_cairn_tokens(bad))
    assert toks == ["cairn/does-not-exist-xyz.md"]
    assert not _resolves(toks[0])


def test_placeholder_tokens_are_skipped():
    text = "the preset source `cairn/templates/onboarding/{preset_name}.md`"
    assert list(_cairn_tokens(text)) == []
