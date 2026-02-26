"""
Aggregation helpers for behavior analytics reports: top pages, scroll depth, clicks, funnels, alerts.
"""
from collections import defaultdict
from datetime import timedelta
from typing import Any

from django.db.models import Avg, Count, F, Q, Sum
from django.utils import timezone

from insights.models import InsightEvent, InsightSession


def _date_range(days: int):
    end = timezone.now()
    start = end - timedelta(days=days)
    return start, end


def top_pages(days: int = 7, limit: int = 20) -> list[dict]:
    """Page views by URL (last N days)."""
    start, end = _date_range(days)
    qs = (
        InsightEvent.objects.filter(
            type='page_view',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('url')
        .annotate(views=Count('id'))
        .order_by('-views')[:limit]
    )
    return [{'url': r['url'], 'views': r['views']} for r in qs]


def avg_time_on_page_by_url(days: int = 7, limit: int = 20) -> list[dict]:
    """Avg time_on_page_ms from page_exit events, by url."""
    start, end = _date_range(days)
    qs = (
        InsightEvent.objects.filter(
            type='page_exit',
            occurred_at__gte=start,
            occurred_at__lte=end,
            payload__time_on_page_ms__isnull=False,
        )
        .values('url')
        .annotate(avg_ms=Avg('payload__time_on_page_ms'))
        .order_by('-avg_ms')[:limit]
    )
    return [{'url': r['url'], 'avg_time_ms': r['avg_ms']} for r in qs]


def scroll_depth_by_page(days: int = 7, milestones: list[int] | None = None) -> list[dict]:
    """For each URL: % of sessions that reached 50% and 90% scroll (by session)."""
    milestones = milestones or [50, 90]
    start, end = _date_range(days)
    # Events: scroll_depth with payload.max_scroll_pct
    scroll_events = (
        InsightEvent.objects.filter(
            type='scroll_depth',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('session_id', 'url', 'payload')
    )
    # per (session, url) max scroll pct
    session_url_max: dict[tuple[int, str], float] = {}
    for e in scroll_events:
        key = (e['session_id'], e['url'])
        pct = (e.get('payload') or {}).get('max_scroll_pct') or 0
        if isinstance(pct, (int, float)):
            session_url_max[key] = max(session_url_max.get(key, 0), float(pct))

    # page_view count per url (sessions that viewed page)
    page_views = (
        InsightEvent.objects.filter(
            type='page_view',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('url')
        .annotate(sessions=Count('session_id', distinct=True))
    )
    pv_by_url = {r['url']: r['sessions'] for r in page_views}

    # per url: sessions reaching each milestone
    url_milestone_count: dict[str, dict[int, set]] = defaultdict(lambda: defaultdict(set))
    for (sid, url), max_pct in session_url_max.items():
        for m in milestones:
            if max_pct >= m:
                url_milestone_count[url][m].add(sid)

    out = []
    for url, sessions_total in pv_by_url.items():
        if sessions_total == 0:
            continue
        row = {'url': url, 'sessions': sessions_total}
        for m in milestones:
            count = len(url_milestone_count[url].get(m, set()))
            row[f'reached_{m}_pct'] = round(100.0 * count / sessions_total, 1)
        out.append(row)
    limit_val = 30
    return sorted(out, key=lambda x: -x['sessions'])[:limit_val]


def scroll_depth_by_page_simple(days: int = 7, limit: int = 30) -> list[dict]:
    """Simpler: per URL, share of scroll_depth events that have max_scroll_pct >= 50 and >= 90."""
    start, end = _date_range(days)
    from django.db.models import Case, When, IntegerField
    events = (
        InsightEvent.objects.filter(
            type='scroll_depth',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('url')
        .annotate(
            total=Count('id'),
            reached_50=Count('id', filter=Q(payload__max_scroll_pct__gte=50)),
            reached_90=Count('id', filter=Q(payload__max_scroll_pct__gte=90)),
        )
    )
    out = []
    for r in events:
        total = r['total'] or 1
        out.append({
            'url': r['url'],
            'sessions_with_scroll': r['total'],
            'reached_50_pct': round(100.0 * (r['reached_50'] or 0) / total, 1),
            'reached_90_pct': round(100.0 * (r['reached_90'] or 0) / total, 1),
        })
    return sorted(out, key=lambda x: -x['sessions_with_scroll'])[:limit]


def top_cta_clicks(days: int = 7, limit: int = 20) -> list[dict]:
    """Top clicked elements (data-track or tag); aggregate by data_track value or selector."""
    start, end = _date_range(days)
    clicks = (
        InsightEvent.objects.filter(
            type='click',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('url', 'payload')
    )
    # Group by (url, data_track or 'tag:id' or 'tag:class')
    key_count: dict[tuple[str, str], int] = defaultdict(int)
    for c in clicks:
        url = c.get('url') or ''
        p = c.get('payload') or {}
        key = p.get('data_track') or p.get('id') or p.get('tag') or 'unknown'
        key = (key or 'unknown')[:200]
        key_count[(url, key)] += 1
    sorted_items = sorted(key_count.items(), key=lambda x: -x[1])[:limit]
    return [
        {'url': url, 'selector': sel, 'clicks': cnt}
        for (url, sel), cnt in sorted_items
    ]


def click_rate_per_page(days: int = 7, limit: int = 30) -> list[dict]:
    """CTA clicks / page views per URL."""
    start, end = _date_range(days)
    views = (
        InsightEvent.objects.filter(type='page_view', occurred_at__gte=start, occurred_at__lte=end)
        .values('url')
        .annotate(views=Count('id'))
    )
    clicks = (
        InsightEvent.objects.filter(type='click', occurred_at__gte=start, occurred_at__lte=end)
        .values('url')
        .annotate(clicks=Count('id'))
    )
    view_map = {r['url']: r['views'] for r in views}
    click_map = {r['url']: r['clicks'] for r in clicks}
    out = []
    for url, v in view_map.items():
        c = click_map.get(url, 0)
        rate = round(100.0 * c / v, 1) if v else 0
        out.append({'url': url, 'page_views': v, 'cta_clicks': c, 'click_rate_pct': rate})
    return sorted(out, key=lambda x: -x['page_views'])[:limit]


def funnel_conversion(
    steps: list[str],
    days: int = 28,
) -> list[dict]:
    """
    steps: list of URL path prefixes (e.g. ['/', '/packages/', '/contact/', '/quote/']).
    For each step, count unique sessions that reached that step (in order).
    """
    start, end = _date_range(days)
    page_views = (
        InsightEvent.objects.filter(
            type='page_view',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('session_id', 'url', 'occurred_at')
        .order_by('session_id', 'occurred_at')
    )
    # session_id -> list of (url, ts) in order
    session_urls: dict[int, list[tuple[str, int]]] = defaultdict(list)
    for e in page_views:
        session_urls[e['session_id']].append((e['url'], e['occurred_at'].timestamp()))
    for sid in session_urls:
        session_urls[sid].sort(key=lambda x: x[1])

    step_counts = []
    for i, prefix in enumerate(steps):
        reached = set()
        for sid, urls in session_urls.items():
            # Check if this session hit step 0..i in order
            idx = 0
            for url, _ in urls:
                if idx <= i and url.startswith(prefix) if prefix != '/' else (url == prefix or url.rstrip('/') == prefix.rstrip('/')):
                    # Normalize: prefix match
                    if prefix == '/':
                        if url == '/' or url.rstrip('/').count('/') <= 1:
                            idx = 1
                    elif url.startswith(prefix):
                        idx = i + 1
                    break
            if idx > i:
                reached.add(sid)
        step_counts.append({'step': prefix, 'sessions': len(reached)})
    return step_counts


def funnel_conversion_simple(
    step_prefixes: list[str],
    days: int = 28,
) -> list[dict]:
    """Simpler funnel: count sessions that have at least one page_view matching each prefix in order."""
    start, end = _date_range(days)
    from django.db.models import Min
    # Get min occurred_at per (session, url) for page_views
    events = (
        InsightEvent.objects.filter(
            type='page_view',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('session_id', 'url')
        .annotate(first_at=Min('occurred_at'))
    )
    session_steps: dict[int, list[tuple[str, Any]]] = defaultdict(list)
    for e in events:
        url = e['url']
        for i, prefix in enumerate(step_prefixes):
            if prefix == '/' and (url == '/' or url.rstrip('/') == ''):
                session_steps[e['session_id']].append((i, e['first_at']))
                break
            if prefix != '/' and url.startswith(prefix):
                session_steps[e['session_id']].append((i, e['first_at']))
                break
    # For each step, count sessions that have reached that step (have an event for step 0..k in order)
    result = []
    for k, prefix in enumerate(step_prefixes):
        count = sum(
            1 for sid, steps in session_steps.items()
            if any(s[0] == k for s in steps)
        )
        result.append({'step': prefix, 'sessions': count})
    return result


def rage_click_alerts(days: int = 7, min_count: int = 3) -> list[dict]:
    """Elements with many rage_click events (possible UX bug)."""
    start, end = _date_range(days)
    rage = (
        InsightEvent.objects.filter(
            type='rage_click',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('url', 'payload')
        .annotate(cnt=Count('id'))
        .filter(cnt__gte=min_count)
    )
    return [
        {
            'url': r['url'],
            'payload': r.get('payload'),
            'count': r['cnt'],
        }
        for r in rage
    ]


def low_cta_pages(days: int = 7, min_views: int = 50, max_click_rate: float = 2.0) -> list[dict]:
    """Pages with high views but low CTA click rate (candidates for UX improvement)."""
    rows = click_rate_per_page(days=days, limit=100)
    return [
        r for r in rows
        if r['page_views'] >= min_views and r['click_rate_pct'] < max_click_rate
    ]


def low_scroll_pages(days: int = 7, min_sessions: int = 20, max_reached_25: float = 25.0) -> list[dict]:
    """Pages where most sessions don't reach 25% scroll."""
    start, end = _date_range(days)
    from django.db.models import Count, Q
    events = (
        InsightEvent.objects.filter(
            type='scroll_depth',
            occurred_at__gte=start,
            occurred_at__lte=end,
        )
        .values('url')
        .annotate(
            total=Count('id'),
            reached_25=Count('id', filter=Q(payload__max_scroll_pct__gte=25)),
        )
    )
    out = []
    for r in events:
        total = r['total'] or 1
        pct = 100.0 * (r['reached_25'] or 0) / total
        if total >= min_sessions and pct < max_reached_25:
            out.append({'url': r['url'], 'sessions': total, 'reached_25_pct': round(pct, 1)})
    return out
