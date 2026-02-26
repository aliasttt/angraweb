"""
Tests for SEO Health snapshot and alert rules.
"""
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone

from insights.models import (
    GSCPageStat,
    InsightSession,
    InsightEvent,
    MetaAuditResult,
    SEOHealthSnapshot,
    InsightAlert,
)
from insights.services.seo_health import (
    compute_gsc_summary,
    compute_behavior_summary,
    compute_meta_issues,
    compute_opportunities,
    check_alerts,
    build_and_save_snapshot,
)


class SEOHealthSnapshotTest(TestCase):
    """Test snapshot calculation and storage."""

    def test_compute_gsc_summary_empty(self):
        start = date.today() - timedelta(days=28)
        end = date.today()
        summary = compute_gsc_summary(start, end)
        self.assertEqual(summary['clicks'], 0)
        self.assertEqual(summary['impressions'], 0)
        self.assertEqual(summary['avg_ctr'], 0)
        self.assertEqual(summary['avg_position'], 0)

    def test_compute_gsc_summary_with_data(self):
        d = date.today()
        GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=10, impressions=200, ctr=0.05, position=5.0)
        start = d - timedelta(days=1)
        summary = compute_gsc_summary(start, d)
        self.assertEqual(summary['clicks'], 10)
        self.assertEqual(summary['impressions'], 200)
        self.assertIsInstance(summary['avg_ctr'], (int, float))
        self.assertEqual(summary['avg_position'], 5.0)

    def test_compute_behavior_summary_empty(self):
        start = date.today() - timedelta(days=7)
        end = date.today()
        summary = compute_behavior_summary(start, end)
        self.assertEqual(summary['sessions'], 0)
        self.assertEqual(summary['pageviews'], 0)
        self.assertEqual(summary['total_clicks'], 0)

    def test_compute_meta_issues_empty(self):
        counts, pages = compute_meta_issues()
        self.assertEqual(counts, {})
        self.assertEqual(pages, [])

    def test_compute_meta_issues_with_data(self):
        MetaAuditResult.objects.create(
            url='https://example.com/page/',
            issues_json=['missing_title', 'missing_description', 'no_h1'],
        )
        counts, pages = compute_meta_issues()
        self.assertIn('missing_title', counts)
        self.assertIn('missing_description', counts)
        self.assertIn('h1_issues', counts)
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]['count'], 3)

    def test_build_and_save_snapshot(self):
        today = timezone.now().date()
        GSCPageStat.objects.create(
            date=today,
            page='https://example.com/',
            clicks=5,
            impressions=100,
            ctr=0.05,
            position=4.0,
        )
        snapshot = build_and_save_snapshot(gsc_days=28, behavior_days=7)
        self.assertIsNotNone(snapshot.pk)
        self.assertEqual(snapshot.gsc_json['clicks'], 5)
        self.assertEqual(snapshot.gsc_json['impressions'], 100)
        self.assertIsInstance(snapshot.behavior_json, dict)
        self.assertIn('sessions', snapshot.behavior_json)
        self.assertIn('pageviews', snapshot.behavior_json)
        self.assertIsInstance(snapshot.opportunities_json, list)
        self.assertIsInstance(snapshot.ux_issues_json, list)
        self.assertIsInstance(snapshot.meta_issues_json, dict)


class SEOHealthAlertTest(TestCase):
    """Test alert thresholds (clicks drop >30%, impressions drop >30%, meta issues +20%)."""

    def test_clicks_drop_alert_triggered(self):
        """When current period has 30%+ fewer clicks than previous, alert is created."""
        today = date.today()
        # Previous 28 days: 100 clicks total
        for i in range(14):
            d = today - timedelta(days=35 + i)
            GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=7, impressions=100, ctr=0.07, position=5.0)
        # Current 28 days: 60 clicks total (< 70% of 100)
        for i in range(14):
            d = today - timedelta(days=14 + i)
            GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=4, impressions=80, ctr=0.05, position=5.0)
        alerts = check_alerts(gsc_days=28, drop_pct_threshold=30)
        click_alerts = [a for a in alerts if a['rule_key'] == 'clicks_drop_30']
        self.assertGreaterEqual(len(click_alerts), 1)
        self.assertIn('Clicks dropped', click_alerts[0]['message'])
        self.assertEqual(InsightAlert.objects.filter(rule_key='clicks_drop_30').count(), 1)

    def test_impressions_drop_alert_triggered(self):
        """When current period has 30%+ fewer impressions, alert is created."""
        today = date.today()
        for i in range(14):
            d = today - timedelta(days=35 + i)
            GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=5, impressions=200, ctr=0.025, position=5.0)
        for i in range(14):
            d = today - timedelta(days=14 + i)
            GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=3, impressions=100, ctr=0.03, position=5.0)
        alerts = check_alerts(gsc_days=28, drop_pct_threshold=30)
        imp_alerts = [a for a in alerts if a['rule_key'] == 'impressions_drop_30']
        self.assertGreaterEqual(len(imp_alerts), 1)
        self.assertEqual(InsightAlert.objects.filter(rule_key='impressions_drop_30').count(), 1)

    def test_no_alert_when_above_threshold(self):
        """When drop is less than 30%, no click/impression alert."""
        InsightAlert.objects.all().delete()
        today = date.today()
        # Previous: 100 clicks
        for i in range(10):
            d = today - timedelta(days=35 + i)
            GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=10, impressions=100, ctr=0.1, position=5.0)
        # Current: 80 clicks (only 20% drop)
        for i in range(10):
            d = today - timedelta(days=14 + i)
            GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=8, impressions=100, ctr=0.08, position=5.0)
        alerts = check_alerts(gsc_days=28, drop_pct_threshold=30)
        click_alerts = [a for a in alerts if a['rule_key'] == 'clicks_drop_30']
        self.assertEqual(len(click_alerts), 0)
        self.assertEqual(InsightAlert.objects.filter(rule_key='clicks_drop_30').count(), 0)
