"""
Ingest behavior events from POST /insights/collect/.
Validates payload, rate limits, allowlist origin/host, bulk_create events.
"""
import hashlib
import json
import logging
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from insights.models import InsightEvent, InsightSession

logger = logging.getLogger(__name__)

MAX_EVENTS_PER_REQUEST = 20
RATE_LIMIT_KEY_PREFIX = 'insights_collect_'
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW_SECONDS = 60
PAYLOAD_MAX_BYTES = 100_000


def _ip_hash(ip: str) -> str:
    """Hash IP for storage; do not store raw IP."""
    if not ip:
        return ''
    return hashlib.sha256(ip.encode() + b'insights_salt').hexdigest()


def _allowed_origins() -> list[str]:
    """Allowed origins for collect endpoint (from settings or env)."""
    val = getattr(settings, 'INSIGHTS_COLLECT_ALLOWED_ORIGINS', None)
    if val is not None:
        return list(val) if isinstance(val, (list, tuple)) else [val]
    env = getattr(settings, 'INSIGHTS_COLLECT_ALLOWED_ORIGINS_ENV', None) or 'INSIGHTS_COLLECT_ALLOWED_ORIGINS'
    raw = getattr(settings, env, None) or __import__('os').environ.get(env, '')
    if not raw:
        return []
    return [x.strip() for x in str(raw).split(',') if x.strip()]


def _allowed_hosts() -> list[str]:
    """Allowed Host header values. Defaults to ALLOWED_HOSTS."""
    val = getattr(settings, 'INSIGHTS_COLLECT_ALLOWED_HOSTS', None)
    if val is not None:
        return list(val) if isinstance(val, (list, tuple)) else [val]
    return list(getattr(settings, 'ALLOWED_HOSTS', []) or [])


def check_origin(origin: str | None, host: str | None) -> tuple[bool, str]:
    """
    Validate Origin and Host. Return (True, '') if allowed else (False, reason).
    """
    allowed_origins = _allowed_origins()
    allowed_hosts = _allowed_hosts()
    if not allowed_origins and not allowed_hosts:
        # No allowlist configured: allow same-origin only (no Origin or Host check in dev)
        if not origin and not host:
            return True, ''
        if host and (not allowed_hosts or host in allowed_hosts):
            return True, ''
        if origin and host:
            return True, ''  # permissive when unset
    if allowed_hosts and host and host not in allowed_hosts:
        return False, 'host_not_allowed'
    if allowed_origins and origin and origin not in allowed_origins:
        return False, 'origin_not_allowed'
    return True, ''


def check_rate_limit(ip: str) -> tuple[bool, str]:
    """Return (True, '') if under limit else (False, 'rate_limit')."""
    key = RATE_LIMIT_KEY_PREFIX + _ip_hash(ip)
    count = cache.get(key, 0)
    if count >= RATE_LIMIT_REQUESTS:
        return False, 'rate_limit'
    return True, ''


def increment_rate_limit(ip: str) -> None:
    key = RATE_LIMIT_KEY_PREFIX + _ip_hash(ip)
    count = cache.get(key, 0)
    cache.set(key, count + 1, timeout=RATE_LIMIT_WINDOW_SECONDS)


def validate_payload(data: bytes) -> tuple[dict | None, str]:
    """
    Parse and validate JSON body. Returns (payload_dict, '') or (None, error_message).
    """
    if len(data) > PAYLOAD_MAX_BYTES:
        return None, 'payload_too_large'
    try:
        payload = json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return None, 'invalid_json'
    if not isinstance(payload, dict):
        return None, 'invalid_payload'
    sid = payload.get('sid')
    events = payload.get('events')
    if not sid:
        return None, 'missing_sid'
    if not isinstance(events, list):
        return None, 'missing_events'
    if len(events) > MAX_EVENTS_PER_REQUEST:
        return None, 'too_many_events'
    allowed_types = {'page_view', 'scroll_depth', 'click', 'page_exit', 'rage_click'}
    for i, ev in enumerate(events):
        if not isinstance(ev, dict):
            return None, f'event_{i}_not_object'
        t = ev.get('type')
        if t not in allowed_types:
            return None, f'event_{i}_invalid_type'
        if not isinstance(ev.get('payload', {}), dict):
            return None, f'event_{i}_invalid_payload'
    return payload, ''


def process_events(
    sid: str,
    cid: str,
    events: list[dict],
    user_agent: str,
    ip_hash_val: str,
    referrer: str,
    consent: bool,
) -> int:
    """
    Get or create session, create InsightEvent records. Returns number of events created.
    """
    from django.utils.dateparse import parse_datetime
    session = InsightSession.objects.filter(sid=sid).first()
    now = timezone.now()
    if not session:
        session = InsightSession(
            sid=sid,
            cid=(cid or '')[:64],
            first_seen=now,
            last_seen=now,
            user_agent=(user_agent or '')[:512],
            ip_hash=ip_hash_val,
            referrer=(referrer or '')[:2048],
            consent=consent,
        )
        session.save()
    else:
        session.last_seen = now
        session.user_agent = (user_agent or '')[:512]
        session.referrer = (referrer or '')[:2048]
        session.consent = consent
        session.save(update_fields=['last_seen', 'user_agent', 'referrer', 'consent'])

    to_create = []
    for ev in events:
        url = (ev.get('url') or '')[:2048]
        ts = ev.get('ts')
        if ts:
            try:
                if isinstance(ts, (int, float)):
                    from datetime import datetime
                    occurred_at = timezone.make_aware(datetime.utcfromtimestamp(ts / 1000.0))
                else:
                    occurred_at = parse_datetime(ts) or now
            except Exception:
                occurred_at = now
        else:
            occurred_at = now
        payload = ev.get('payload')
        if not isinstance(payload, dict):
            payload = {}
        to_create.append(
            InsightEvent(
                session=session,
                type=ev.get('type', 'page_view'),
                url=url,
                occurred_at=occurred_at,
                payload=payload,
            )
        )
    if to_create:
        InsightEvent.objects.bulk_create(to_create)
    return len(to_create)
