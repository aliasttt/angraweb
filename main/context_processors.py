"""
Context processor: canonical URL همیشه با دامنهٔ canonical (https، بدون www) برای ایندکس بهتر.
"""
from django.conf import settings


def canonical_url(request):
    """آدرس canonical یکسان برای همهٔ درخواست‌ها (حل مشکل Duplicate canonical در GSC)."""
    canonical_domain = getattr(settings, 'CANONICAL_DOMAIN', '').strip()
    if canonical_domain:
        path = request.get_full_path()
        return {'canonical_url': canonical_domain + path}
    return {'canonical_url': request.build_absolute_uri()}
