"""
Admin dashboard view: SEO (GSC KPIs, top queries/pages, alerts) + Behavior + SEO Health snapshot.
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.conf import settings
import os

from insights.services.gsc_reports import (
    gsc_kpis,
    gsc_top_queries_with_delta,
    gsc_top_pages_with_delta,
    gsc_alerts,
)
from insights.services.analytics_reports import (
    top_pages,
    avg_time_on_page_by_url,
    scroll_depth_by_page_simple,
    top_cta_clicks,
    click_rate_per_page,
    funnel_conversion_simple,
    rage_click_alerts,
    low_cta_pages,
    low_scroll_pages,
)
from insights.models import SEOHealthSnapshot, InsightAlert


def get_funnel_steps():
    """Funnel step path prefixes from settings or default."""
    steps = getattr(settings, 'INSIGHTS_FUNNEL_STEPS', None)
    if steps is not None:
        return list(steps)
    env = os.environ.get('INSIGHTS_FUNNEL_STEPS', '')
    if env:
        return [s.strip() for s in env.split(',') if s.strip()]
    return ['/', '/packages/', '/contact/', '/quote/']


@staff_member_required
def admin_dashboard(request):
    """Single dashboard with SEO and Behavior tabs/sections."""
    # SEO (GSC)
    kpis_7 = gsc_kpis(7)
    kpis_28 = gsc_kpis(28)
    top_queries = gsc_top_queries_with_delta(7, limit=10)
    top_pages_gsc = gsc_top_pages_with_delta(7, limit=10)
    seo_alerts = gsc_alerts(7)

    # Behavior
    behavior_top_pages = top_pages(7, limit=15)
    avg_time = avg_time_on_page_by_url(7, limit=15)
    scroll_by_page = scroll_depth_by_page_simple(7, limit=15)
    cta_clicks = top_cta_clicks(7, limit=15)
    click_rate = click_rate_per_page(7, limit=20)
    funnel_steps = get_funnel_steps()
    funnel = funnel_conversion_simple(funnel_steps, days=28)
    rage_alerts = rage_click_alerts(7, min_count=2)
    low_cta = low_cta_pages(7, min_views=20, max_click_rate=2.0)
    low_scroll = low_scroll_pages(7, min_sessions=10, max_reached_25=25.0)

    # SEO Health: latest snapshot + recent alerts
    latest_snapshot = SEOHealthSnapshot.objects.order_by('-snapshot_at').first()
    recent_alerts = list(InsightAlert.objects.order_by('-created_at')[:15])

    context = {
        'kpis_7': kpis_7,
        'kpis_28': kpis_28,
        'top_queries': top_queries,
        'top_pages_gsc': top_pages_gsc,
        'seo_alerts': seo_alerts,
        'latest_snapshot': latest_snapshot,
        'recent_alerts': recent_alerts,
        'behavior_top_pages': behavior_top_pages,
        'avg_time': avg_time,
        'scroll_by_page': scroll_by_page,
        'cta_clicks': cta_clicks,
        'click_rate': click_rate,
        'funnel_steps': funnel_steps,
        'funnel': funnel,
        'rage_alerts': rage_alerts,
        'low_cta': low_cta,
        'low_scroll': low_scroll,
    }
    return render(request, 'insights/admin_dashboard.html', context)


@staff_member_required
def seo_health_dashboard(request):
    """SEO Health snapshot dashboard: KPIs, opportunities, UX issues, meta issues, alerts."""
    latest = SEOHealthSnapshot.objects.order_by('-snapshot_at').first()
    recent_alerts = list(InsightAlert.objects.order_by('-created_at')[:20])
    context = {
        'snapshot': latest,
        'recent_alerts': recent_alerts,
    }
    return render(request, 'insights/seo_health_dashboard.html', context)
