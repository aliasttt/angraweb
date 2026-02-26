"""
Clear all Insights data (GSC, behavior, meta audit, SERP). No sample data is loaded.
Use when you want only real data from GSC sync and tracker.
Usage: python manage.py insights_clear_data
"""
from django.core.management.base import BaseCommand

from insights.models import (
    GSCQueryPageStat,
    GSCPageStat,
    InsightSession,
    InsightEvent,
    MetaAuditResult,
    SerpSnapshot,
)


class Command(BaseCommand):
    help = 'Clear all Insights data (no sample load). Use before adding real data only.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Do not ask for confirmation',
        )

    def handle(self, *args, **options):
        if not options.get('no_input'):
            confirm = input('Delete ALL Insights data? (yes/no): ')
            if confirm.lower() not in ('yes', 'y'):
                self.stdout.write('Cancelled.')
                return

        counts = {}
        counts['events'] = InsightEvent.objects.count()
        InsightEvent.objects.all().delete()
        counts['sessions'] = InsightSession.objects.count()
        InsightSession.objects.all().delete()
        counts['gsc_qp'] = GSCQueryPageStat.objects.count()
        GSCQueryPageStat.objects.all().delete()
        counts['gsc_p'] = GSCPageStat.objects.count()
        GSCPageStat.objects.all().delete()
        counts['meta'] = MetaAuditResult.objects.count()
        MetaAuditResult.objects.all().delete()
        counts['serp'] = SerpSnapshot.objects.count()
        SerpSnapshot.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Cleared: {counts["events"]} events, {counts["sessions"]} sessions, '
                f'{counts["gsc_qp"]} GSC query+page, {counts["gsc_p"]} GSC page, '
                f'{counts["meta"]} meta audit, {counts["serp"]} SERP.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS('Insights is empty. Add real data: insights_sync_gsc, tracker, insights_audit_meta.')
        )
