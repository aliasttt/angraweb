"""
Compute and save SEO Health snapshot (GSC + behavior + meta), run alert rules.
Usage: python manage.py insights_seo_health_snapshot --days 28
"""
from django.core.management.base import BaseCommand
from insights.services.seo_health import build_and_save_snapshot


class Command(BaseCommand):
    help = 'Compute SEO Health summary and save snapshot; run alert rules (e.g. clicks drop >30%)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=28,
            help='GSC period in days (default: 28). Behavior uses last 7 days.',
        )

    def handle(self, *args, **options):
        days = options.get('days', 28)
        snapshot = build_and_save_snapshot(gsc_days=days, behavior_days=7)
        self.stdout.write(
            self.style.SUCCESS(
                f'SEO Health snapshot saved: {snapshot.snapshot_at}. '
                f'GSC {snapshot.gsc_start_date}–{snapshot.gsc_end_date}, '
                f'Behavior {snapshot.behavior_start_date}–{snapshot.behavior_end_date}.'
            )
        )
