"""
Sync Google Search Console data for the last N days.
Usage: python manage.py insights_sync_gsc --days 28
"""
import logging
from django.core.management.base import BaseCommand
from insights.services.gsc import sync_gsc

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch GSC search analytics (query+page and page) and upsert into DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=None,
            help='Number of days to sync (default: INSIGHTS_GSC_DAYS_DEFAULT or 28)',
        )

    def handle(self, *args, **options):
        days = options.get('days')
        try:
            c1, c2 = sync_gsc(days=days)
            self.stdout.write(self.style.SUCCESS(f'GSC sync done: query+page={c1}, page={c2}'))
        except Exception as e:
            logger.exception('GSC sync failed: %s', e)
            self.stdout.write(self.style.ERROR(f'GSC sync failed: {e}'))
