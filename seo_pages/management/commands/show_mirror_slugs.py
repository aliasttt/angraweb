"""
Print mirror slug mapping for a service (for debugging language switcher).
Usage: python manage.py show_mirror_slugs web-design
"""
from django.core.management.base import BaseCommand

from ...silo_config import get_mirrored_slug, SERVICE_SILO_MAP


class Command(BaseCommand):
    help = "Print TR<->EN cluster mirror slugs for a service (for debugging)."

    def add_arguments(self, parser):
        parser.add_argument("service_key", type=str, help="e.g. web-design")

    def handle(self, *args, **options):
        service_key = options["service_key"]
        if service_key not in SERVICE_SILO_MAP:
            self.stdout.write(self.style.ERROR(f"Unknown service: {service_key}"))
            return
        tr_clusters = SERVICE_SILO_MAP[service_key]["tr"].get("clusters", [])
        en_clusters = SERVICE_SILO_MAP[service_key]["en"].get("clusters", [])
        self.stdout.write(f"TR clusters (n={len(tr_clusters)}): {tr_clusters}")
        self.stdout.write(f"EN clusters (n={len(en_clusters)}): {en_clusters}")
        self.stdout.write("")
        self.stdout.write("TR slug -> EN mirror (get_mirrored_slug):")
        for i, tr_slug in enumerate(tr_clusters):
            en_slug = get_mirrored_slug(service_key, "cluster", "tr", tr_slug)
            en_idx = en_clusters.index(en_slug) if en_slug and en_slug in en_clusters else -1
            self.stdout.write(f"  [{i}] {tr_slug} -> {en_slug} (EN idx={en_idx})")
        self.stdout.write("")
        self.stdout.write("EN slug -> TR mirror (get_mirrored_slug):")
        for i, en_slug in enumerate(en_clusters):
            tr_slug = get_mirrored_slug(service_key, "cluster", "en", en_slug)
            tr_idx = tr_clusters.index(tr_slug) if tr_slug and tr_slug in tr_clusters else -1
            self.stdout.write(f"  [{i}] {en_slug} -> {tr_slug} (TR idx={tr_idx})")
