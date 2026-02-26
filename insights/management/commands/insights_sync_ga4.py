"""
Optional: Sync GA4 data. Stub when not fully implemented.
Usage: python manage.py insights_sync_ga4 --days 28
"""
from django.core.management.base import BaseCommand
from insights.services.ga4 import sync_ga4


class Command(BaseCommand):
    help = 'Fetch GA4 data (optional); stub if not configured'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=28, help='Days to sync')

    def handle(self, *args, **options):
        count = sync_ga4(days=options['days'])
        self.stdout.write(self.style.SUCCESS(f'GA4 sync done: {count}'))
