"""
GA4 (Google Analytics 4) optional integration.
Only used when INSIGHTS_GA4_PROPERTY_ID and INSIGHTS_GA4_CREDENTIALS_JSON are set.
Stub: minimal MVP for users/sessions/engagement by day.
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def is_ga4_configured() -> bool:
    prop_id = getattr(settings, 'INSIGHTS_GA4_PROPERTY_ID', None) or os.environ.get('INSIGHTS_GA4_PROPERTY_ID')
    creds = getattr(settings, 'INSIGHTS_GA4_CREDENTIALS_JSON', None) or os.environ.get('INSIGHTS_GA4_CREDENTIALS_JSON')
    return bool(prop_id and creds)


def _get_ga4_client():
    """Return GA4 Data API client or None."""
    if not is_ga4_configured():
        return None
    prop_id = getattr(settings, 'INSIGHTS_GA4_PROPERTY_ID', None) or os.environ.get('INSIGHTS_GA4_PROPERTY_ID')
    creds_json = getattr(settings, 'INSIGHTS_GA4_CREDENTIALS_JSON', None) or os.environ.get('INSIGHTS_GA4_CREDENTIALS_JSON')
    try:
        from google.oauth2 import service_account
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
    except ImportError:
        logger.warning('google-analytics-data not installed; GA4 sync disabled.')
        return None
    try:
        if creds_json.strip().startswith('{'):
            creds_dict = json.loads(creds_json)
        else:
            with open(os.path.expanduser(creds_json), 'r') as f:
                creds_dict = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        client = BetaAnalyticsDataClient(credentials=credentials)
        return client, prop_id
    except Exception as e:
        logger.exception('GA4 credentials error: %s', e)
        return None


def sync_ga4(days: int = 28) -> int:
    """
    Stub: Run GA4 sync. Returns 0 (no GA4 model in MVP to keep scope minimal).
    When extending: add model GA4DailyStat(date, users, sessions, engagement_seconds, page_path optional).
    """
    if not is_ga4_configured():
        return 0
    client_info = _get_ga4_client()
    if not client_info:
        return 0
    # Placeholder: could run run_report for activeUsers, sessions, engagementTime by date
    logger.info('GA4 sync stub: configured but no storage model (MVP).')
    return 0
