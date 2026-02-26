"""
SEO Health: weekly summary (GSC + behavior + meta), opportunities, UX issues, alerts.
Uses GSCPageStat, InsightSession/InsightEvent, MetaAuditResult. No external deps.
"""
from datetime import timedelta, datetime
from collections import defaultdict

from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone

from insights.models import (
    GSCPageStat,
    InsightSession,
    InsightEvent,
    MetaAuditResult,
    SEOHealthSnapshot,
    InsightAlert,
)


def _date_range_days(days: int):
    end = timezone.now().date()
    start = end - timedelta(days=days)
    return start, end


def _datetime_range_days(days: int):
    end = timezone.now()
    start = end - timedelta(days=days)
    return start, end


# ─── GSC (from GSCPageStat only) ─────────────────────────────────────────────

def compute_gsc_summary(gsc_start, gsc_end) -> dict:
    """Aggregate GSCPageStat for date range. Returns clicks, impressions, avg_ctr, avg_position."""
    qs = GSCPageStat.objects.filter(date__gte=gsc_start, date__lte=gsc_end).aggregate(
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


# ─── Behavior (last 7 days) ──────────────────────────────────────────────────

def compute_behavior_summary(behavior_start, behavior_end) -> dict:
    """Sessions, pageviews, avg scroll depth (max_scroll_pct), total clicks."""
    start_dt = timezone.make_aware(datetime.combine(behavior_start, datetime.min.time()))
    end_dt = timezone.make_aware(datetime.combine(behavior_end, datetime.max.time()))

    sessions_count = InsightSession.objects.filter(
        last_seen__gte=start_dt,
        last_seen__lte=end_dt,
    ).count()

    pageviews = InsightEvent.objects.filter(
        type='page_view',
        occurred_at__gte=start_dt,
        occurred_at__lte=end_dt,
    ).count()

    clicks_count = InsightEvent.objects.filter(
        type='click',
        occurred_at__gte=start_dt,
        occurred_at__lte=end_dt,
    ).count()

    scroll_events = list(
        InsightEvent.objects.filter(
            type='scroll_depth',
            occurred_at__gte=start_dt,
            occurred_at__lte=end_dt,
        ).values_list('payload', flat=True)
    )
    scroll_pcts = []
    for p in scroll_events:
        if isinstance(p, dict) and isinstance(p.get('max_scroll_pct'), (int, float)):
            scroll_pcts.append(float(p['max_scroll_pct']))
    avg_scroll = round(sum(scroll_pcts) / len(scroll_pcts), 1) if scroll_pcts else 0

    return {
        'sessions': sessions_count,
        'pageviews': pageviews,
        'total_clicks': clicks_count,
        'avg_scroll_depth_pct': avg_scroll,
    }


# ─── Meta audit issues ───────────────────────────────────────────────────────

def compute_meta_issues() -> tuple[dict, list]:
    """Count issues by type from latest MetaAuditResult per URL (or all). Returns (counts_dict, top_pages_list)."""
    results = MetaAuditResult.objects.all().order_by('url', '-checked_at')
    seen_urls = set()
    issue_counts = defaultdict(int)
    pages_with_issues = []

    for r in results:
        if r.url in seen_urls:
            continue
        seen_urls.add(r.url)
        issues = r.issues_json or []
        for issue in issues:
            if isinstance(issue, str):
                if issue.startswith('missing_title'):
                    issue_counts['missing_title'] += 1
                elif issue.startswith('missing_description'):
                    issue_counts['missing_description'] += 1
                elif issue.startswith('multiple_h1') or issue == 'no_h1':
                    issue_counts['h1_issues'] += 1
                elif 'canonical' in issue.lower() or issue == 'no_canonical':
                    issue_counts['canonical'] += 1
                elif 'noindex' in issue.lower():
                    issue_counts['noindex'] += 1
                else:
                    issue_counts['other'] += 1
        if issues:
            pages_with_issues.append({
                'url': r.url[:200],
                'issues': issues[:10],
                'count': len(issues),
            })

    pages_with_issues.sort(key=lambda x: -x['count'])
    return dict(issue_counts), pages_with_issues[:30]


# ─── Opportunities (GSC) ─────────────────────────────────────────────────────

def compute_opportunities(gsc_start, gsc_end, site_avg_ctr: float, limit: int = 20) -> list[dict]:
    """High impressions low CTR; position <= 10 but CTR below site avg."""
    qs = (
        GSCPageStat.objects.filter(date__gte=gsc_start, date__lte=gsc_end)
        .values('page')
        .annotate(
            clicks=Sum('clicks'),
            impressions=Sum('impressions'),
            avg_ctr=Avg('ctr'),
            avg_position=Avg('position'),
        )
        .filter(impressions__gte=10)
    )
    opportunities = []
    for r in qs:
        ctr_pct = (r['avg_ctr'] or 0) * 100
        pos = r['avg_position'] or 99
        reason = None
        if site_avg_ctr > 0 and ctr_pct < site_avg_ctr * 0.7 and r['impressions'] >= 50:
            reason = 'high_impressions_low_ctr'
        elif pos <= 10 and site_avg_ctr > 0 and ctr_pct < site_avg_ctr * 0.8:
            reason = 'position_top10_low_ctr'
        if reason:
            opportunities.append({
                'page': r['page'][:500],
                'clicks': r['clicks'],
                'impressions': r['impressions'],
                'ctr_pct': round(ctr_pct, 2),
                'position': round(pos, 1),
                'reason': reason,
            })
    opportunities.sort(key=lambda x: (-x['impressions'], x['ctr_pct']))
    return opportunities[:limit]


# ─── UX issues (behavior) ────────────────────────────────────────────────────

def compute_ux_issues(behavior_start, behavior_end, min_pageviews: int = 30, limit: int = 20) -> list[dict]:
    """Pages with high pageviews but low scroll or low click rate."""
    start_dt = timezone.make_aware(datetime.combine(behavior_start, datetime.min.time()))
    end_dt = timezone.make_aware(datetime.combine(behavior_end, datetime.max.time()))

    views = (
        InsightEvent.objects.filter(type='page_view', occurred_at__gte=start_dt, occurred_at__lte=end_dt)
        .values('url')
        .annotate(views=Count('id'))
    )
    view_map = {r['url']: r['views'] for r in views}

    clicks = (
        InsightEvent.objects.filter(type='click', occurred_at__gte=start_dt, occurred_at__lte=end_dt)
        .values('url')
        .annotate(clicks=Count('id'))
    )
    click_map = {r['url']: r['clicks'] for r in clicks}

    scroll = (
        InsightEvent.objects.filter(
            type='scroll_depth',
            occurred_at__gte=start_dt,
            occurred_at__lte=end_dt,
        )
        .values('url')
        .annotate(
            total=Count('id'),
            reached_50=Count('id', filter=Q(payload__max_scroll_pct__gte=50)),
        )
    )
    scroll_map = {}
    for r in scroll:
        total = r['total'] or 1
        scroll_map[r['url']] = {'total': r['total'], 'reached_50_pct': round(100.0 * (r['reached_50'] or 0) / total, 1)}

    ux_issues = []
    for url, v in view_map.items():
        if v < min_pageviews:
            continue
        c = click_map.get(url, 0)
        click_rate = round(100.0 * c / v, 1) if v else 0
        scroll_info = scroll_map.get(url, {'reached_50_pct': 0})
        reached_50 = scroll_info['reached_50_pct']
        if reached_50 < 30 or click_rate < 2.0:
            ux_issues.append({
                'url': url[:500],
                'pageviews': v,
                'click_rate_pct': click_rate,
                'reached_50_scroll_pct': reached_50,
            })
    ux_issues.sort(key=lambda x: (-x['pageviews'], x['reached_50_scroll_pct'], x['click_rate_pct']))
    return ux_issues[:limit]


# ─── Alert rules ─────────────────────────────────────────────────────────────

def check_alerts(gsc_days: int, drop_pct_threshold: float = 30, meta_issues_increase_pct: float = 20) -> list[dict]:
    """
    Compare current vs previous period. Returns list of alert dicts (rule_key, severity, message, context).
    Creates InsightAlert records.
    """
    start, end = _date_range_days(gsc_days)
    prev_start = start - timedelta(days=gsc_days)

    curr_gsc = compute_gsc_summary(start, end)
    prev_gsc = compute_gsc_summary(prev_start, start - timedelta(days=1))

    alerts_created = []

    prev_clicks = prev_gsc['clicks'] or 0
    curr_clicks = curr_gsc['clicks'] or 0
    if prev_clicks > 0 and (curr_clicks - prev_clicks) / prev_clicks * 100 <= -drop_pct_threshold:
        pct = round((1 - curr_clicks / prev_clicks) * 100, 1)
        msg = f'Clicks dropped {pct}% vs previous {gsc_days}-day period.'
        alerts_created.append({
            'rule_key': 'clicks_drop_30',
            'severity': 'warning',
            'message': msg,
            'context': {'curr_clicks': curr_clicks, 'prev_clicks': prev_clicks, 'pct': pct},
        })

    prev_imp = prev_gsc['impressions'] or 0
    curr_imp = curr_gsc['impressions'] or 0
    if prev_imp > 0 and (curr_imp - prev_imp) / prev_imp * 100 <= -drop_pct_threshold:
        pct = round((1 - curr_imp / prev_imp) * 100, 1)
        msg = f'Impressions dropped {pct}% vs previous {gsc_days}-day period.'
        alerts_created.append({
            'rule_key': 'impressions_drop_30',
            'severity': 'warning',
            'message': msg,
            'context': {'curr_impressions': curr_imp, 'prev_impressions': prev_imp, 'pct': pct},
        })

    prev_snapshot = SEOHealthSnapshot.objects.filter(
        gsc_end_date__lte=start - timedelta(days=1),
    ).order_by('-snapshot_at').first()
    curr_meta_counts, _ = compute_meta_issues()
    curr_meta_total = sum(curr_meta_counts.values())
    if prev_snapshot and prev_snapshot.meta_issues_json:
        prev_meta_total = sum(prev_snapshot.meta_issues_json.values()) if isinstance(prev_snapshot.meta_issues_json, dict) else 0
        if prev_meta_total > 0 and curr_meta_total >= prev_meta_total * (1 + meta_issues_increase_pct / 100):
            pct = round((curr_meta_total - prev_meta_total) / prev_meta_total * 100, 1)
            msg = f'Meta issues increased {pct}% vs previous snapshot.'
            alerts_created.append({
                'rule_key': 'meta_issues_increase_20',
                'severity': 'info',
                'message': msg,
                'context': {'curr_total': curr_meta_total, 'prev_total': prev_meta_total},
            })

    for a in alerts_created:
        InsightAlert.objects.create(
            severity=a['severity'],
            rule_key=a['rule_key'],
            message=a['message'],
            context_json=a['context'],
        )
    return alerts_created


# ─── Main: build and save snapshot ───────────────────────────────────────────

def build_and_save_snapshot(gsc_days: int = 28, behavior_days: int = 7) -> SEOHealthSnapshot:
    """Compute full SEO health summary and save SEOHealthSnapshot. Run alert rules and create InsightAlerts."""
    gsc_start, gsc_end = _date_range_days(gsc_days)
    behavior_start, behavior_end = _date_range_days(behavior_days)

    gsc_summary = compute_gsc_summary(gsc_start, gsc_end)
    behavior_summary = compute_behavior_summary(behavior_start, behavior_end)
    meta_counts, meta_pages = compute_meta_issues()

    site_avg_ctr = gsc_summary['avg_ctr'] or 0
    opportunities = compute_opportunities(gsc_start, gsc_end, site_avg_ctr, limit=20)
    ux_issues = compute_ux_issues(behavior_start, behavior_end, min_pageviews=30, limit=20)

    check_alerts(gsc_days, drop_pct_threshold=30, meta_issues_increase_pct=20)

    snapshot = SEOHealthSnapshot.objects.create(
        snapshot_at=timezone.now(),
        gsc_start_date=gsc_start,
        gsc_end_date=gsc_end,
        behavior_start_date=behavior_start,
        behavior_end_date=behavior_end,
        gsc_json=gsc_summary,
        behavior_json=behavior_summary,
        meta_issues_json=meta_counts,
        opportunities_json=opportunities,
        ux_issues_json=ux_issues,
        meta_issues_pages_json=meta_pages,
    )
    return snapshot
