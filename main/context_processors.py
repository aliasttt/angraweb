"""
Context processor: canonical URL and hreflang alternates for SEO.
Canonical and hreflang use CANONICAL_DOMAIN (prefer https).
"""
from django.conf import settings


def canonical_url(request):
    """Canonical URL (domain + path) and hreflang alternates for language-prefixed SEO. Prefers https when CANONICAL_DOMAIN is set."""
    canonical_domain = getattr(settings, 'CANONICAL_DOMAIN', '').strip().rstrip('/')
    if canonical_domain and canonical_domain.startswith('http://'):
        canonical_domain = 'https://' + canonical_domain[7:]
    if not canonical_domain:
        return {
            'canonical_url': request.build_absolute_uri(request.path),
            'hreflang_urls': None,
        }
    path = request.path
    # Path is e.g. /tr/about/ or /en/contact/ — use as-is for canonical
    canonical_url_value = canonical_domain + path

    # Build alternate URLs for tr, en, x-default only when on a language-prefixed page
    path_stripped = path.rstrip('/') or '/'
    parts = path_stripped.strip('/').split('/')
    hreflang_urls = None
    if parts and parts[0] in ('tr', 'en'):
        path_without_lang = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'
        if path_without_lang != '/' and not path_without_lang.endswith('/'):
            path_without_lang += '/'
        lang_codes = [code for code, _ in getattr(settings, 'LANGUAGES', [('tr', 'Turkish'), ('en', 'English')])]
        hreflang_urls = []
        for code in lang_codes:
            hreflang_urls.append((code, canonical_domain + f'/{code}{path_without_lang}'))
        default_code = getattr(settings, 'LANGUAGE_CODE', 'tr')
        hreflang_urls.append(('x-default', canonical_domain + f'/{default_code}{path_without_lang}'))

    return {
        'canonical_url': canonical_url_value,
        'hreflang_urls': hreflang_urls,
    }
