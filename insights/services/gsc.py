"""
Google Search Console API client.
Fetches search analytics (clicks, impressions, ctr, position) by query+page and by page.
Uses env: INSIGHTS_GSC_SITE_URL, INSIGHTS_GSC_CREDENTIALS_JSON, INSIGHTS_GSC_DAYS_DEFAULT.
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Iterator

from django.conf import settings
from django.utils import timezone

from insights.models import GSCPageStat, GSCQueryPageStat

logger = logging.getLogger(__name__)


def _get_gsc_client():
    """Build GSC API client from credentials. Returns None if not configured."""
    site_url = getattr(settings, 'INSIGHTS_GSC_SITE_URL', None) or os.environ.get('INSIGHTS_GSC_SITE_URL')
    creds_json = getattr(settings, 'INSIGHTS_GSC_CREDENTIALS_JSON', None) or os.environ.get('INSIGHTS_GSC_CREDENTIALS_JSON')
    if not site_url or not creds_json:
        return None, None

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        logger.warning('google-api-python-client not installed; GSC sync disabled.')
        return None, None

    try:
        if creds_json.strip().startswith('{'):
            creds_dict = json.loads(creds_json)
        else:
            with open(os.path.expanduser(creds_json), 'r') as f:
                creds_dict = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        service = build('searchconsole', 'v1', credentials=credentials, cache_discovery=False)
        return service, site_url.strip()
    except Exception as e:
        logger.exception('GSC credentials error: %s', e)
        return None, None


def _parse_row(row: dict, date_str: str) -> dict:
    """Convert API row to dict with date and metrics."""
    keys = row.get('keys', [])
    clicks = int(row.get('clicks', 0))
    impressions = int(row.get('impressions', 0))
    ctr = float(row.get('ctr', 0))
    position = float(row.get('position', 0))
    return {
        'date': datetime.strptime(date_str, '%Y-%m-%d').date(),
        'keys': keys,
        'clicks': clicks,
        'impressions': impressions,
        'ctr': ctr,
        'position': position,
    }


def _fetch_search_analytics(
    service: Any,
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: list[str],
) -> Iterator[dict]:
    """Yield rows from searchanalytics.query. Paginates with startRow."""
    start_row = 0
    page_size = 25000
    while True:
        body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': page_size,
            'startRow': start_row,
        }
        try:
            resp = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
        except Exception as e:
            logger.exception('GSC API request failed: %s', e)
            raise
        rows = resp.get('rows', [])
        if not rows:
            break
        for row in rows:
            yield row
        if len(rows) < page_size:
            break
        start_row += page_size


def fetch_query_page_stats(
    service: Any,
    site_url: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[dict]:
    """Fetch (date, query, page) rows and return list of dicts for upsert."""
    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    out = []
    for row in _fetch_search_analytics(
        service, site_url, start_str, end_str,
        dimensions=['date', 'query', 'page'],
    ):
        keys = row.get('keys', [])
        if len(keys) < 3:
            continue
        date_str, query, page = keys[0], keys[1], keys[2]
        out.append({
            'date': datetime.strptime(date_str, '%Y-%m-%d').date(),
            'query': (query or '')[:500],
            'page': (page or '')[:2048],
            'clicks': int(row.get('clicks', 0)),
            'impressions': int(row.get('impressions', 0)),
            'ctr': float(row.get('ctr', 0)),
            'position': float(row.get('position', 0)),
        })
    return out


def fetch_page_stats(
    service: Any,
    site_url: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[dict]:
    """Fetch (date, page) rows and return list of dicts for upsert."""
    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    out = []
    for row in _fetch_search_analytics(
        service, site_url, start_str, end_str,
        dimensions=['date', 'page'],
    ):
        keys = row.get('keys', [])
        if len(keys) < 2:
            continue
        date_str, page = keys[0], keys[1]
        out.append({
            'date': datetime.strptime(date_str, '%Y-%m-%d').date(),
            'page': (page or '')[:2048],
            'clicks': int(row.get('clicks', 0)),
            'impressions': int(row.get('impressions', 0)),
            'ctr': float(row.get('ctr', 0)),
            'position': float(row.get('position', 0)),
        })
    return out


def upsert_query_page_stats(items: list[dict]) -> int:
    """Bulk upsert GSCQueryPageStat by (date, query, page)."""
    if not items:
        return 0
    to_create = []
    for d in items:
        obj, _ = GSCQueryPageStat.objects.update_or_create(
            date=d['date'],
            query=d['query'],
            page=d['page'],
            defaults={
                'clicks': d['clicks'],
                'impressions': d['impressions'],
                'ctr': d['ctr'],
                'position': d['position'],
            },
        )
        # update_or_create already saves; we only need to track count
    return len(items)


def upsert_page_stats(items: list[dict]) -> int:
    """Bulk upsert GSCPageStat by (date, page)."""
    if not items:
        return 0
    for d in items:
        GSCPageStat.objects.update_or_create(
            date=d['date'],
            page=d['page'],
            defaults={
                'clicks': d['clicks'],
                'impressions': d['impressions'],
                'ctr': d['ctr'],
                'position': d['position'],
            },
        )
    return len(items)


def sync_gsc(days: int | None = None) -> tuple[int, int]:
    """
    Fetch GSC data for the last `days` days and upsert.
    Returns (count_query_page, count_page).
    """
    days = days or int(
        getattr(settings, 'INSIGHTS_GSC_DAYS_DEFAULT', None)
        or os.environ.get('INSIGHTS_GSC_DAYS_DEFAULT', '28')
    )
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    service, site_url = _get_gsc_client()
    if not service or not site_url:
        logger.warning('GSC not configured; skip sync.')
        return 0, 0

    logger.info('GSC sync: %s to %s', start_date, end_date)
    try:
        qp_rows = fetch_query_page_stats(service, site_url, start_date, end_date)
        p_rows = fetch_page_stats(service, site_url, start_date, end_date)
        c1 = upsert_query_page_stats(qp_rows)
        c2 = upsert_page_stats(p_rows)
        logger.info('GSC sync done: query+page=%s, page=%s', c1, c2)
        return c1, c2
    except Exception as e:
        logger.exception('GSC sync failed: %s', e)
        raise
