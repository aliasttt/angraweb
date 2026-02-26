"""
SERP snapshot service (SerpApi or similar). Behind feature flag INSIGHTS_ENABLE_SERP=1.
Env: INSIGHTS_SERPAPI_KEY, INSIGHTS_SERP_LOCATION, INSIGHTS_SERP_KEYWORDS (comma-separated).
"""
import json
import logging
import os
from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone
import requests

from insights.models import SerpSnapshot

logger = logging.getLogger(__name__)


def is_serp_enabled() -> bool:
    val = getattr(settings, 'INSIGHTS_ENABLE_SERP', None) or os.environ.get('INSIGHTS_ENABLE_SERP', '0')
    return str(val) in ('1', 'true', 'yes')


def _get_serp_config() -> dict | None:
    if not is_serp_enabled():
        return None
    key = getattr(settings, 'INSIGHTS_SERPAPI_KEY', None) or os.environ.get('INSIGHTS_SERPAPI_KEY')
    if not key:
        return None
    location = getattr(settings, 'INSIGHTS_SERP_LOCATION', None) or os.environ.get('INSIGHTS_SERP_LOCATION', 'Istanbul, Turkey')
    keywords_str = getattr(settings, 'INSIGHTS_SERP_KEYWORDS', None) or os.environ.get('INSIGHTS_SERP_KEYWORDS', '')
    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
    return {'api_key': key, 'location': location, 'keywords': keywords}


def fetch_serp_for_keyword(api_key: str, keyword: str, location: str) -> dict | None:
    """Call SerpApi Google Organic Results. Returns JSON response or None."""
    url = 'https://serpapi.com/search'
    params = {
        'q': keyword,
        'location': location,
        'api_key': api_key,
        'engine': 'google',
        'num': 10,
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning('SerpApi request failed for "%s": %s', keyword, e)
        return None


def extract_organic_top10(data: dict) -> list[dict]:
    """Extract top 10 organic results from SerpApi response."""
    organic = data.get('organic_results', [])[:10]
    return [
        {
            'position': i + 1,
            'title': r.get('title', ''),
            'url': r.get('link', ''),
        }
        for i, r in enumerate(organic)
    ]


def our_domain_rank(results: list[dict], our_domain: str) -> int | None:
    """Return 1-based rank if our domain appears in any result URL, else None."""
    if not our_domain:
        return None
    domain = our_domain.replace('https://', '').replace('http://', '').split('/')[0].lower()
    for r in results:
        url = (r.get('url') or '').lower()
        if domain in url:
            return r.get('position')
    return None


def sync_serp(our_domain: str | None = None) -> int:
    """
    Fetch SERP for configured keywords and store SerpSnapshot.
    our_domain: e.g. 'https://example.com' to compute our_domain_rank.
    """
    config = _get_serp_config()
    if not config or not config['keywords']:
        return 0
    api_key = config['api_key']
    location = config['location']
    count = 0
    for keyword in config['keywords']:
        data = fetch_serp_for_keyword(api_key, keyword, location)
        if not data:
            continue
        results = extract_organic_top10(data)
        rank = our_domain_rank(results, our_domain or '') if our_domain else None
        SerpSnapshot.objects.create(
            keyword=keyword,
            location=location,
            checked_at=timezone.now(),
            results_json=results,
            our_domain_rank=rank,
        )
        count += 1
    return count
