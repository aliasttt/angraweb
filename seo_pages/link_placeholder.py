"""
Internal link placeholder parsing and normalization.
Used by templatetags (render at display) and management command (normalize in DB).
"""
from __future__ import annotations

import re
from typing import List, Optional, Tuple

# Match all supported placeholder forms: { link:... }, {link:...}, {{ link:... }}, {{link:...}}
PLACEHOLDER_PATTERN = re.compile(
    r"\{\{?\s*link:\s*([^\}]+)\s*\}\}?",
    re.IGNORECASE,
)

CANONICAL_TEMPLATE = "{{ link:%s }}"


def find_placeholders(html: str) -> List[Tuple[int, int, str]]:
    """Return list of (start, end, path) for each placeholder. Path is stripped."""
    out = []
    for m in PLACEHOLDER_PATTERN.finditer(html):
        path = (m.group(1) or "").strip()
        out.append((m.start(), m.end(), path))
    return out


def normalize_placeholders(html: str) -> str:
    """Rewrite any placeholder variant to canonical form {{ link:PATH }}. Path gets trailing / if missing."""
    if not html:
        return html
    result = []
    last = 0
    for start, end, path in find_placeholders(html):
        path = path.rstrip("/")
        if path:
            path = path + "/"
        result.append(html[last:start])
        result.append(CANONICAL_TEMPLATE % path)
        last = end
    result.append(html[last:])
    return "".join(result)


def has_placeholder_syntax(html: str) -> bool:
    """True if content still contains any { link: or {{ link: pattern (for validation)."""
    return bool(PLACEHOLDER_PATTERN.search(html or ""))
