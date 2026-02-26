"""
Context processor: expose insights consent/DNT flags for base template.
"""
from django.conf import settings
import os


def insights_settings(request):
    """Add insights_require_consent and insights_respect_dnt to template context."""
    require = getattr(settings, 'INSIGHTS_REQUIRE_CONSENT', None)
    if require is None:
        require = os.environ.get('INSIGHTS_REQUIRE_CONSENT', '1') in ('1', 'true', 'yes')
    respect_dnt = getattr(settings, 'INSIGHTS_RESPECT_DNT', None)
    if respect_dnt is None:
        respect_dnt = os.environ.get('INSIGHTS_RESPECT_DNT', '0') in ('1', 'true', 'yes')
    return {
        'insights_require_consent': require,
        'insights_respect_dnt': respect_dnt,
    }
