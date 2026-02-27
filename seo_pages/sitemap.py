from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import SeoPage


class SeoPagesLanguageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def __init__(self, language: str):
        self.language = language
        super().__init__()

    def items(self):
        now = timezone.now()
        return (
            SeoPage.objects.filter(language=self.language, is_indexable=True)
            .filter(published_at__isnull=False, published_at__lte=now)
            .select_related("service")
            .only(
                "id",
                "language",
                "page_type",
                "slug",
                "updated_at",
                "published_at",
                "service__key",
                "service__tr_base_path",
                "service__en_base_path",
            )
            .order_by("service__key", "page_type", "slug")
        )

    def location(self, obj: SeoPage) -> str:
        return obj.get_absolute_url()

    def lastmod(self, obj: SeoPage):
        return obj.updated_at


sitemaps = {
    "tr": SeoPagesLanguageSitemap("tr"),
    "en": SeoPagesLanguageSitemap("en"),
}

