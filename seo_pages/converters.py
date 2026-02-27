from __future__ import annotations

import re

from .silo_config import get_service_bases


class TrServiceBaseConverter:
    """
    Match only known Turkish service base paths so we don't shadow /tr/about/, /tr/contact/, etc.
    """

    def __init__(self):
        bases = get_service_bases("tr")
        self.regex = "(?:" + "|".join(re.escape(b) for b in bases) + ")"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value


class EnServiceBaseConverter:
    """
    Match only known English service base paths so we don't shadow /en/about/, /en/contact/, etc.
    """

    def __init__(self):
        bases = get_service_bases("en")
        self.regex = "(?:" + "|".join(re.escape(b) for b in bases) + ")"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value

