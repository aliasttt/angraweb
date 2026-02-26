"""
GSC aggregation helpers for dashboard: KPIs, top queries/pages, deltas, alerts.
"""
from datetime import timedelta
from django.db.models import Avg, Count, Sum
from django.utils import timezone

from insights.models import GSCPageStat, GSCQueryPageStat


def _date_range(days: int):
    end = timezone.now().date()
    start = end - timedelta(days=days)
    return start, end


def gsc_kpis(days: int) -> dict:
    """Total clicks, impressions, avg CTR, avg position for last N days."""
    start, end = _date_range(days)
    qs = GSCPageStat.objects.filter(date__gte=start, date__lte=end).aggregate(
        total_clicks=Sum('clicks'),
        total_impressions=Sum('impressions'),
        avg_ctr=Avg('ctr'),
        avg_position=Avg('position'),
    )
    return {
        'clicks': qs['total_clicks'] or 0,
        'impressions': qs['total_impressions'] or 0,
        'avg_ctr': round((qs['avg_ctr'] or 0) * 100, 2),
        'avg_position': round(qs['avg_position'] or 0, 1),
    }


def gsc_top_queries(days: int = 7, limit: int = 10) -> list[dict]:
    """Top queries by clicks (aggregate over pages)."""
    start, end = _date_range(days)
    from django.db.models import Sum
    qs = (
        GSCQueryPageStat.objects.filter(date__gte=start, date__lte=end)
        .values('query')
        .annotate(clicks=Sum('clicks'), impressions=Sum('impressions'))
        .order_by('-clicks')[:limit]
    )
    return [{'query': r['query'], 'clicks': r['clicks'], 'impressions': r['impressions']} for r in qs]


def gsc_top_pages(days: int = 7, limit: int = 10) -> list[dict]:
    """Top pages by clicks."""
    start, end = _date_range(days)
    qs = (
        GSCPageStat.objects.filter(date__gte=start, date__lte=end)
        .values('page')
        .annotate(clicks=Sum('clicks'), impressions=Sum('impressions'))
        .order_by('-clicks')[:limit]
    )
    return [{'page': r['page'], 'clicks': r['clicks'], 'impressions': r['impressions']} for r in qs]


def gsc_top_queries_with_delta(days: int = 7, limit: int = 10) -> list[dict]:
    """Top queries with delta vs previous period (clicks change)."""
    start, end = _date_range(days)
    prev_start = start - timedelta(days=days)
    from django.db.models import Sum
    current = dict(
        (r['query'], r['clicks'])
        for r in
        GSCQueryPageStat.objects.filter(date__gte=start, date__lte=end)
        .values('query')
        .annotate(clicks=Sum('clicks'))
        .order_by('-clicks')[:limit * 2]
    )
    prev = dict(
        (r['query'], r['clicks'])
        for r in
        GSCQueryPageStat.objects.filter(date__gte=prev_start, date__lte=start - timedelta(days=1))
        .values('query')
        .annotate(clicks=Sum('clicks'))
    )
    out = []
    for q, c in sorted(current.items(), key=lambda x: -x[1])[:limit]:
        p = prev.get(q, 0)
        delta = c - p if p else c
        out.append({'query': q, 'clicks': c, 'prev_clicks': p, 'delta': delta})
    return out


def gsc_top_pages_with_delta(days: int = 7, limit: int = 10) -> list[dict]:
    """Top pages with delta vs previous period."""
    start, end = _date_range(days)
    prev_start = start - timedelta(days=days)
    from django.db.models import Sum
    current = dict(
        (r['page'], r['clicks'])
        for r in
        GSCPageStat.objects.filter(date__gte=start, date__lte=end)
        .values('page')
        .annotate(clicks=Sum('clicks'))
        .order_by('-clicks')[:limit * 2]
    )
    prev = dict(
        (r['page'], r['clicks'])
        for r in
        GSCPageStat.objects.filter(date__gte=prev_start, date__lte=start - timedelta(days=1))
        .values('page')
        .annotate(clicks=Sum('clicks'))
    )
    out = []
    for page, c in sorted(current.items(), key=lambda x: -x[1])[:limit]:
        p = prev.get(page, 0)
        delta = c - p if p else c
        out.append({'page': page, 'clicks': c, 'prev_clicks': p, 'delta': delta})
    return out


def gsc_alerts(days: int = 7, drop_pct_threshold: float = 30, position_worse_threshold: float = 2.0) -> list[dict]:
    """Alerts: big drop in clicks/impressions, or avg position worsened significantly."""
    start, end = _date_range(days)
    prev_start = start - timedelta(days=days)
    curr_kpi = GSCPageStat.objects.filter(date__gte=start, date__lte=end).aggregate(
        clicks=Sum('clicks'), impressions=Sum('impressions'), pos=Avg('position')
    )
    prev_kpi = GSCPageStat.objects.filter(date__gte=prev_start, date__lte=start - timedelta(days=1)).aggregate(
        clicks=Sum('clicks'), impressions=Sum('impressions'), pos=Avg('position')
    )
    alerts = []
    c_c, p_c = curr_kpi['clicks'] or 0, prev_kpi['clicks'] or 0
    if p_c > 0 and (c_c - p_c) / p_c * 100 <= -drop_pct_threshold:
        alerts.append({'type': 'clicks_drop', 'message': f'Clicks dropped {round((1 - c_c/p_c)*100, 1)}% vs previous period.'})
    c_i, p_i = curr_kpi['impressions'] or 0, prev_kpi['impressions'] or 0
    if p_i > 0 and (c_i - p_i) / p_i * 100 <= -drop_pct_threshold:
        alerts.append({'type': 'impressions_drop', 'message': f'Impressions dropped {round((1 - c_i/p_i)*100, 1)}% vs previous period.'})
    curr_pos = curr_kpi['pos'] or 0
    prev_pos = prev_kpi['pos'] or 0
    if prev_pos > 0 and curr_pos - prev_pos >= position_worse_threshold:
        alerts.append({'type': 'position_worse', 'message': f'Avg position worsened from {prev_pos:.1f} to {curr_pos:.1f}.'})
    return alerts
