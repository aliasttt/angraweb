"""
Load sample data for Insights: GSC stats, behavior events, meta audit, optional SERP.
Use for demo/dashboard when real API data is not yet available.
Usage: python manage.py insights_load_sample_data
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from insights.models import (
    GSCQueryPageStat,
    GSCPageStat,
    InsightSession,
    InsightEvent,
    MetaAuditResult,
    SerpSnapshot,
)


# Base URL for sample pages (match your site)
DEFAULT_BASE = 'https://angraweb.com'


class Command(BaseCommand):
    help = 'Load sample data for Insights dashboard and admin sections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--base-url',
            type=str,
            default=DEFAULT_BASE,
            help='Base URL for sample pages (default: https://angraweb.com)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing insights data before loading sample data',
        )

    def handle(self, *args, **options):
        base = (options.get('base_url') or DEFAULT_BASE).rstrip('/')
        clear = options.get('clear', False)

        if clear:
            self.stdout.write('Clearing existing insights data...')
            InsightEvent.objects.all().delete()
            InsightSession.objects.all().delete()
            GSCQueryPageStat.objects.all().delete()
            GSCPageStat.objects.all().delete()
            MetaAuditResult.objects.all().delete()
            SerpSnapshot.objects.all().delete()
            self.stdout.write('Cleared.')
        else:
            # بدون --clear اگر قبلاً دادهٔ نمونه داریم، دوباره اضافه نکن
            if InsightSession.objects.filter(ip_hash__startswith='sample_').exists():
                self.stdout.write(
                    self.style.WARNING(
                        'Sample data already exists. Use --clear to clear and reload once.'
                    )
                )
                return

        # ─── GSC: last 28 days, multiple queries and pages ─────────────────
        queries = [
            'web tasarım', 'kurumsal web sitesi', 'e-ticaret sitesi', 'SEO',
            'web tasarım fiyatları', 'angraweb', 'iletişim', 'paketler',
        ]
        pages = [
            base + '/',
            base + '/packages/',
            base + '/contact/',
            base + '/about/',
            base + '/services/',
            base + '/web-design/',
            base + '/quote/',
        ]
        today = date.today()
        gsc_qp_count = 0
        gsc_p_count = 0
        for d in range(28):
            day = today - timedelta(days=d)
            for page in pages:
                clicks = random.randint(2, 80)
                impressions = random.randint(50, 800)
                ctr = round(clicks / max(impressions, 1), 4)
                pos = round(random.uniform(2.5, 12.0), 1)
                GSCPageStat.objects.update_or_create(
                    date=day, page=page,
                    defaults={'clicks': clicks, 'impressions': impressions, 'ctr': ctr, 'position': pos},
                )
                gsc_p_count += 1
            for q in queries[:5]:
                page = random.choice(pages)
                clicks = random.randint(1, 40)
                impressions = random.randint(20, 400)
                ctr = round(clicks / max(impressions, 1), 4)
                pos = round(random.uniform(1.5, 15.0), 1)
                GSCQueryPageStat.objects.update_or_create(
                    date=day, query=q, page=page,
                    defaults={'clicks': clicks, 'impressions': impressions, 'ctr': ctr, 'position': pos},
                )
                gsc_qp_count += 1
        self.stdout.write(self.style.SUCCESS(f'GSC: {GSCPageStat.objects.count()} page stats, {GSCQueryPageStat.objects.count()} query+page stats.'))

        # ─── Behavior: sessions and events ───────────────────────────────────
        import uuid
        event_types = ['page_view', 'scroll_depth', 'click', 'page_exit', 'rage_click']
        for i in range(12):
            sid = str(uuid.uuid4())
            sess = InsightSession.objects.create(
                sid=sid,
                cid=f'c{i}{random.randint(1000, 9999)}',
                first_seen=timezone.now() - timedelta(days=random.randint(0, 14)),
                last_seen=timezone.now() - timedelta(hours=random.randint(0, 72)),
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                ip_hash='sample_' + str(i),
                referrer='https://www.google.com/' if i % 2 else '',
                consent=True,
            )
            urls = [base + p for p in ['/', '/packages/', '/contact/', '/about/', '/services/']]
            for u in urls[: random.randint(2, 5)]:
                occurred = timezone.now() - timedelta(hours=random.randint(0, 48))
                InsightEvent.objects.create(
                    session=sess, type='page_view', url=u, occurred_at=occurred, payload={},
                )
                if random.random() > 0.3:
                    InsightEvent.objects.create(
                        session=sess, type='scroll_depth', url=u, occurred_at=occurred,
                        payload={'milestone': 50, 'max_scroll_pct': random.choice([25, 50, 75, 90])},
                    )
                if random.random() > 0.5:
                    InsightEvent.objects.create(
                        session=sess, type='click', url=u, occurred_at=occurred,
                        payload={'data_track': 'cta_quote', 'tag': 'a', 'text': 'Teklif Al'},
                    )
                InsightEvent.objects.create(
                    session=sess, type='page_exit', url=u,
                    occurred_at=occurred + timedelta(seconds=random.randint(30, 300)),
                    payload={'time_on_page_ms': random.randint(15000, 120000)},
                )
            if i % 4 == 0:
                InsightEvent.objects.create(
                    session=sess, type='rage_click', url=base + '/contact/',
                    occurred_at=timezone.now() - timedelta(hours=random.randint(1, 24)),
                    payload={'data_track': 'submit_btn', 'text': 'Gönder'},
                )
        self.stdout.write(self.style.SUCCESS(f'Behavior: {InsightSession.objects.count()} sessions, {InsightEvent.objects.count()} events.'))

        # ─── Meta audit ──────────────────────────────────────────────────────
        for path, title, desc in [
            ('/', 'Angraweb | Web Tasarım ve E-ticaret', 'Profesyonel web tasarım, e-ticaret ve SEO hizmetleri.'),
            ('/packages/', 'Paketler | Angraweb', 'Web sitesi ve e-ticaret paketleri. Uygun fiyatlar.'),
            ('/contact/', 'İletişim | Angraweb', 'Bizimle iletişime geçin. Teklif alın.'),
            ('/about/', 'Hakkımızda | Angraweb', 'Angraweb ekibi ve hizmetlerimiz hakkında.'),
        ]:
            MetaAuditResult.objects.get_or_create(
                url=base + path,
                defaults={
                    'checked_at': timezone.now(),
                    'title': title,
                    'description': desc,
                    'h1_count': 1,
                    'canonical': base + path,
                    'status_code': 200,
                    'resp_ms': random.randint(80, 250),
                    'issues_json': [],
                },
            )
        # One with issues
        MetaAuditResult.objects.get_or_create(
            url=base + '/some-old-page/',
            defaults={
                'checked_at': timezone.now(),
                'title': 'Short',
                'description': 'Kısa açıklama',
                'h1_count': 0,
                'status_code': 200,
                'issues_json': ['title_too_short_5', 'description_too_short_15', 'no_h1'],
            },
        )
        self.stdout.write(self.style.SUCCESS(f'Meta audit: {MetaAuditResult.objects.count()} results.'))

        # ─── SERP (optional sample) ──────────────────────────────────────────
        if not SerpSnapshot.objects.filter(keyword='web tasarım', location='Istanbul, Turkey').exists():
            SerpSnapshot.objects.create(
                keyword='web tasarım',
                location='Istanbul, Turkey',
                checked_at=timezone.now(),
                results_json=[
                    {'position': i, 'title': f'Result {i}', 'url': f'https://example.com/{i}'}
                    for i in range(1, 11)
                ],
                our_domain_rank=3,
            )
        self.stdout.write(self.style.SUCCESS(f'SERP: {SerpSnapshot.objects.count()} snapshot(s).'))

        self.stdout.write(self.style.SUCCESS('Sample data loaded. Refresh /admin/insights/ and Insights admin sections.'))
