"""
Unit tests: GSC upsert, collect validation, aggregation.
"""
from datetime import date, timedelta
import json
from django.test import TestCase, override_settings
from django.utils import timezone

from insights.models import GSCQueryPageStat, GSCPageStat, InsightSession, InsightEvent
from insights.services.gsc import upsert_query_page_stats, upsert_page_stats
from insights.services.analytics_ingest import (
    validate_payload,
    check_origin,
    _ip_hash,
    process_events,
)
from insights.services.analytics_reports import top_pages, click_rate_per_page
from insights.services.gsc_reports import gsc_kpis, gsc_top_queries_with_delta


class GSCUpsertTest(TestCase):
    """Test GSC model upsert logic."""

    def test_upsert_query_page_stat(self):
        d = date.today()
        items = [
            {'date': d, 'query': 'q1', 'page': 'https://example.com/a', 'clicks': 10, 'impressions': 100, 'ctr': 0.1, 'position': 2.5},
            {'date': d, 'query': 'q1', 'page': 'https://example.com/a', 'clicks': 15, 'impressions': 120, 'ctr': 0.12, 'position': 2.3},
        ]
        n = upsert_query_page_stats(items)
        self.assertEqual(n, 2)
        self.assertEqual(GSCQueryPageStat.objects.count(), 1)
        row = GSCQueryPageStat.objects.get(date=d, query='q1', page='https://example.com/a')
        self.assertEqual(row.clicks, 15)
        self.assertEqual(row.impressions, 120)

    def test_upsert_page_stat(self):
        d = date.today()
        items = [
            {'date': d, 'page': 'https://example.com/', 'clicks': 5, 'impressions': 50, 'ctr': 0.1, 'position': 3.0},
        ]
        n = upsert_page_stats(items)
        self.assertEqual(n, 1)
        self.assertEqual(GSCPageStat.objects.count(), 1)
        row = GSCPageStat.objects.get(date=d, page='https://example.com/')
        self.assertEqual(row.clicks, 5)


class CollectValidationTest(TestCase):
    """Test ingest endpoint validation."""

    def test_validate_payload_ok(self):
        body = json.dumps({
            'sid': '550e8400-e29b-41d4-a716-446655440000',
            'events': [
                {'type': 'page_view', 'url': 'https://example.com/', 'payload': {}},
            ],
        }).encode('utf-8')
        payload, err = validate_payload(body)
        self.assertEqual(err, '')
        self.assertIsNotNone(payload)
        self.assertEqual(payload['sid'], '550e8400-e29b-41d4-a716-446655440000')
        self.assertEqual(len(payload['events']), 1)

    def test_validate_payload_missing_sid(self):
        body = json.dumps({'events': []}).encode('utf-8')
        payload, err = validate_payload(body)
        self.assertIsNotNone(err)
        self.assertIn('sid', err)

    def test_validate_payload_missing_events(self):
        body = json.dumps({'sid': '550e8400-e29b-41d4-a716-446655440000'}).encode('utf-8')
        payload, err = validate_payload(body)
        self.assertIsNotNone(err)

    def test_validate_payload_invalid_type(self):
        body = json.dumps({
            'sid': '550e8400-e29b-41d4-a716-446655440000',
            'events': [{'type': 'invalid_type', 'payload': {}}],
        }).encode('utf-8')
        payload, err = validate_payload(body)
        self.assertIsNotNone(err)

    def test_validate_payload_too_many_events(self):
        body = json.dumps({
            'sid': '550e8400-e29b-41d4-a716-446655440000',
            'events': [{'type': 'page_view', 'payload': {}}] * 25,
        }).encode('utf-8')
        payload, err = validate_payload(body)
        self.assertIsNotNone(err)
        self.assertIn('too_many', err)

    @override_settings(
        INSIGHTS_COLLECT_ALLOWED_ORIGINS=['https://example.com'],
        INSIGHTS_COLLECT_ALLOWED_HOSTS=['example.com'],
    )
    def test_check_origin_allowed(self):
        ok, reason = check_origin('https://example.com', 'example.com')
        self.assertTrue(ok, reason)

    @override_settings(
        INSIGHTS_COLLECT_ALLOWED_ORIGINS=['https://example.com'],
        INSIGHTS_COLLECT_ALLOWED_HOSTS=['example.com'],
    )
    def test_check_origin_rejected(self):
        ok, reason = check_origin('https://evil.com', 'evil.com')
        self.assertFalse(ok)
        self.assertIn('allowed', reason)

    def test_ip_hash(self):
        h = _ip_hash('192.168.1.1')
        self.assertTrue(isinstance(h, str) and len(h) == 64)


class CollectProcessTest(TestCase):
    """Test process_events creates session and events."""

    def test_process_events_creates_session_and_events(self):
        sid = '550e8400-e29b-41d4-a716-446655440000'
        events = [
            {'type': 'page_view', 'url': 'https://example.com/', 'payload': {}},
            {'type': 'click', 'url': 'https://example.com/', 'payload': {'data_track': 'cta'}},
        ]
        n = process_events(
            sid=sid,
            cid='',
            events=events,
            user_agent='Test',
            ip_hash_val='abc',
            referrer='',
            consent=True,
        )
        self.assertEqual(n, 2)
        self.assertEqual(InsightSession.objects.count(), 1)
        self.assertEqual(InsightEvent.objects.count(), 2)


class AnalyticsReportsTest(TestCase):
    """Test aggregation functions."""

    def test_top_pages_empty(self):
        result = top_pages(days=7, limit=10)
        self.assertEqual(result, [])

    def test_top_pages_with_data(self):
        session = InsightSession.objects.create(sid='550e8400-e29b-41d4-a716-446655440001', consent=True)
        for _ in range(3):
            InsightEvent.objects.create(session=session, type='page_view', url='https://example.com/a', payload={})
        for _ in range(2):
            InsightEvent.objects.create(session=session, type='page_view', url='https://example.com/b', payload={})
        result = top_pages(days=30, limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['url'], 'https://example.com/a')
        self.assertEqual(result[0]['views'], 3)
        self.assertEqual(result[1]['views'], 2)

    def test_click_rate_per_page(self):
        session = InsightSession.objects.create(sid='550e8400-e29b-41d4-a716-446655440002', consent=True)
        for _ in range(4):
            InsightEvent.objects.create(session=session, type='page_view', url='https://example.com/p', payload={})
        for _ in range(2):
            InsightEvent.objects.create(session=session, type='click', url='https://example.com/p', payload={})
        result = click_rate_per_page(days=30, limit=10)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['page_views'], 4)
        self.assertEqual(result[0]['cta_clicks'], 2)
        self.assertEqual(result[0]['click_rate_pct'], 50.0)


class GSCReportsTest(TestCase):
    """Test GSC report helpers."""

    def test_gsc_kpis_empty(self):
        kpis = gsc_kpis(7)
        self.assertEqual(kpis['clicks'], 0)
        self.assertEqual(kpis['impressions'], 0)

    def test_gsc_kpis_with_data(self):
        d = date.today()
        GSCPageStat.objects.create(date=d, page='https://example.com/', clicks=10, impressions=100, ctr=0.05, position=5.0)
        kpis = gsc_kpis(7)
        self.assertEqual(kpis['clicks'], 10)
        self.assertEqual(kpis['impressions'], 100)

    def test_gsc_top_queries_with_delta(self):
        d = date.today()
        prev = d - timedelta(days=14)
        GSCQueryPageStat.objects.create(date=d, query='q1', page='https://example.com/', clicks=20, impressions=200, ctr=0.1, position=2.0)
        GSCQueryPageStat.objects.create(date=prev, query='q1', page='https://example.com/', clicks=10, impressions=100, ctr=0.1, position=2.0)
        result = gsc_top_queries_with_delta(days=7, limit=10)
        self.assertGreaterEqual(len(result), 1)
        self.assertEqual(result[0]['query'], 'q1')
        self.assertEqual(result[0]['clicks'], 20)
        self.assertEqual(result[0]['prev_clicks'], 10)
        self.assertEqual(result[0]['delta'], 10)
