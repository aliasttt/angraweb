"""
Collect endpoint: POST /insights/collect/
Accepts JSON: { sid, cid?, events: [{ type, url?, ts?, payload? }, ...] }
Rate limit, origin/host allowlist, bulk_create events.
"""
import json
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from insights.services.analytics_ingest import (
    check_origin,
    check_rate_limit,
    increment_rate_limit,
    validate_payload,
    process_events,
    _ip_hash,
)

logger = logging.getLogger(__name__)


def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_http_methods(['POST', 'OPTIONS']), name='dispatch')
class CollectView(View):
    """POST /insights/collect/ — ingest behavior events."""

    def options(self, request):
        return HttpResponse(status=204, headers={
            'Access-Control-Allow-Origin': request.headers.get('Origin', '*'),
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '86400',
        })

    def post(self, request):
        origin = request.META.get('HTTP_ORIGIN') or ''
        host = request.META.get('HTTP_HOST') or ''
        ok, reason = check_origin(origin, host)
        if not ok:
            return JsonResponse({'ok': False, 'error': reason}, status=403)

        ip = _get_client_ip(request)
        ok, reason = check_rate_limit(ip)
        if not ok:
            return JsonResponse({'ok': False, 'error': reason}, status=429)

        body = request.body
        payload, err = validate_payload(body)
        if err:
            return JsonResponse({'ok': False, 'error': err}, status=400)

        sid = payload.get('sid')
        cid = payload.get('cid') or ''
        events = payload.get('events', [])
        if not sid or not events:
            return JsonResponse({'ok': False, 'error': 'missing_sid_or_events'}, status=400)

        try:
            sid_str = str(sid) if sid else ''
        except Exception:
            return JsonResponse({'ok': False, 'error': 'invalid_sid'}, status=400)

        user_agent = request.META.get('HTTP_USER_AGENT', '')[:512]
        referrer = request.META.get('HTTP_REFERER', '')[:2048]
        consent = payload.get('consent', False) is True

        try:
            count = process_events(
                sid=sid_str,
                cid=(cid or '')[:64],
                events=events,
                user_agent=user_agent,
                ip_hash_val=_ip_hash(ip),
                referrer=referrer,
                consent=consent,
            )
            increment_rate_limit(ip)
            return JsonResponse({'ok': True, 'count': count})
        except Exception as e:
            logger.exception('Collect process_events failed: %s', e)
            return JsonResponse({'ok': False, 'error': 'server_error'}, status=500)
