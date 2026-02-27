from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .link_placeholder import has_placeholder_syntax


class Service(models.Model):
    """
    Core service category shared across TR/EN silos.

    IMPORTANT: this is intentionally separate from `main.Service`.
    """

    key = models.SlugField(
        max_length=64,
        unique=True,
        help_text='Stable internal key (e.g. "web-design").',
    )

    tr_name = models.CharField(max_length=200)
    tr_base_path = models.SlugField(
        max_length=120,
        help_text='Base path after /tr/ (e.g. "web-tasarim").',
    )

    en_name = models.CharField(max_length=200)
    en_base_path = models.SlugField(
        max_length=120,
        help_text='Base path after /en/ (e.g. "web-design").',
    )

    class Meta:
        verbose_name = "SEO Service"
        verbose_name_plural = "SEO Services"

    def __str__(self) -> str:  # pragma: no cover
        return self.key

    def name_for_language(self, language: str) -> str:
        if language == "tr":
            return self.tr_name
        if language == "en":
            return self.en_name
        raise ValueError("language must be 'tr' or 'en'")

    def base_path_for_language(self, language: str) -> str:
        if language == "tr":
            return self.tr_base_path
        if language == "en":
            return self.en_base_path
        raise ValueError("language must be 'tr' or 'en'")


class SeoPage(models.Model):
    LANGUAGE_TR = "tr"
    LANGUAGE_EN = "en"
    LANGUAGE_CHOICES = [
        (LANGUAGE_TR, "Turkish"),
        (LANGUAGE_EN, "English"),
    ]

    TYPE_PILLAR = "pillar"
    TYPE_PRICING = "pricing"
    TYPE_GUIDE = "guide"
    TYPE_CLUSTER = "cluster"
    TYPE_QUOTE = "quote"
    PAGE_TYPE_CHOICES = [
        (TYPE_PILLAR, "Pillar"),
        (TYPE_PRICING, "Pricing"),
        (TYPE_GUIDE, "Guide"),
        (TYPE_CLUSTER, "Cluster"),
        (TYPE_QUOTE, "Quote"),
    ]

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="seo_pages")
    page_type = models.CharField(max_length=16, choices=PAGE_TYPE_CHOICES)

    # Pillar uses empty slug. Pricing/Guide/Quote use fixed slugs; Cluster uses a normal slug.
    slug = models.SlugField(max_length=160, blank=True, default="")

    title = models.CharField(max_length=300, help_text="H1")
    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.TextField(blank=True)

    # Auto: self-referential (store as path, e.g. /tr/web-tasarim/).
    # Stored as CharField because URLField rejects relative paths.
    canonical_url = models.CharField(max_length=500, blank=True)

    og_title = models.CharField(max_length=300, blank=True)
    og_description = models.TextField(blank=True)

    content_html = models.TextField(blank=True)
    faq_json = models.JSONField(
        default=list,
        blank=True,
        help_text='List of {"question": "...", "answer": "..."} objects.',
    )

    is_indexable = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("language", "service", "page_type", "slug"),)
        indexes = [
            models.Index(fields=["language", "service", "page_type", "slug"]),
            models.Index(fields=["language", "is_indexable", "published_at"]),
        ]
        verbose_name = "SEO Page"
        verbose_name_plural = "SEO Pages"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.language}:{self.service.key}:{self.page_type}:{self.slug or '(pillar)'}"

    @property
    def is_published(self) -> bool:
        return self.published_at is not None and self.published_at <= timezone.now()

    def fixed_slug_for_page_type(self) -> str:
        if self.page_type == self.TYPE_PILLAR:
            return ""
        if self.page_type == self.TYPE_PRICING:
            return "fiyatlar" if self.language == "tr" else "pricing"
        if self.page_type == self.TYPE_GUIDE:
            return "rehber" if self.language == "tr" else "guide"
        if self.page_type == self.TYPE_QUOTE:
            return "teklif-al" if self.language == "tr" else "get-quote"
        return ""

    def get_absolute_url(self) -> str:
        base = f"/{self.language}/{self.service.base_path_for_language(self.language)}/"
        if self.page_type == self.TYPE_PILLAR:
            return base
        if not self.slug:
            return base
        return f"{base}{self.slug}/"

    def clean(self):
        super().clean()

        if self.language not in ("tr", "en"):
            raise ValidationError({"language": "Language must be 'tr' or 'en'."})

        # Enforce fixed slugs for page types.
        if self.page_type in (self.TYPE_PILLAR, self.TYPE_PRICING, self.TYPE_GUIDE, self.TYPE_QUOTE):
            expected = self.fixed_slug_for_page_type()
            if (self.slug or "") != expected:
                raise ValidationError({"slug": f"Slug must be '{expected}' for {self.page_type} pages."})

        # Prevent reserved slugs from being used as clusters.
        if self.page_type == self.TYPE_CLUSTER:
            reserved = {
                "fiyatlar",
                "pricing",
                "rehber",
                "guide",
                "teklif-al",
                "get-quote",
            }
            if (self.slug or "") in reserved:
                raise ValidationError({"slug": "This slug is reserved for non-cluster page types."})
            if not self.slug:
                raise ValidationError({"slug": "Cluster pages require a slug."})

        # Language-safe rule: no cross-language body links inside content_html.
        html = self.content_html or ""
        if self.language == "tr":
            if re.search(r'(["\'])/en/', html) or "https://angraweb.com/en/" in html or "http://angraweb.com/en/" in html:
                raise ValidationError({"content_html": "Turkish pages cannot link to /en/ inside body content_html."})
        if self.language == "en":
            if re.search(r'(["\'])/tr/', html) or "https://angraweb.com/tr/" in html or "http://angraweb.com/tr/" in html:
                raise ValidationError({"content_html": "English pages cannot link to /tr/ inside body content_html."})

        # FAQ shape sanity check (avoid breaking template/schema).
        if self.faq_json:
            if not isinstance(self.faq_json, list):
                raise ValidationError({"faq_json": "faq_json must be a list."})
            for i, item in enumerate(self.faq_json):
                if not isinstance(item, dict) or "question" not in item or "answer" not in item:
                    raise ValidationError({"faq_json": f"Invalid FAQ item at index {i}."})

        # Unreplaced link placeholders must not be saved (run seo_pages_cleanup_and_upgrade to replace with HTML).
        if html and has_placeholder_syntax(html):
            raise ValidationError(
                {"content_html": "Content contains link placeholders (e.g. { link:... }). Run management command seo_pages_cleanup_and_upgrade to replace with HTML, or replace manually."}
            )

        # Pricing intent: non-pricing pages should not contain pricing-heavy language.
        if self.page_type != self.TYPE_PRICING and html:
            # Ignore text inside <a>...</a> (anchor text) to avoid flagging link text like "fiyatlar"
            body_only = re.sub(r"<a\b[^>]*>.*?</a>", " ", html, flags=re.DOTALL | re.IGNORECASE)
            text_lower = re.sub(r"<[^>]+>", " ", body_only).lower()
            tr_triggers = ["fiyat", "ücret", "maliyet", "paket"]
            en_triggers = ["price", "pricing", "cost", "package"]
            triggers = en_triggers if self.language == "en" else tr_triggers
            if any(t in text_lower for t in triggers):
                raise ValidationError(
                    {"content_html": "Pricing intent detected outside pricing page. Move pricing language to the pricing page and link to it."}
                )

        # Duplicate content: same service+language with identical body.
        if html and self.service_id:
            dup = SeoPage.objects.filter(
                service_id=self.service_id,
                language=self.language,
                content_html=html,
            ).exclude(pk=self.pk).exists()
            if dup:
                raise ValidationError(
                    {"content_html": "Another page in this service and language has identical content. Ensure unique content per URL."}
                )

    def save(self, *args, **kwargs):
        # Keep canonical_url self-referential by default (path). Templates will render absolute canonical.
        if not self.canonical_url:
            self.canonical_url = self.get_absolute_url()
        super().save(*args, **kwargs)


class InternalLinkRule(models.Model):
    """
    Optional helper for managing internal link anchors per language/service.
    """

    language = models.CharField(max_length=2, choices=SeoPage.LANGUAGE_CHOICES)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="internal_link_rules")
    from_page_type = models.CharField(max_length=16, choices=SeoPage.PAGE_TYPE_CHOICES)
    to_page_type = models.CharField(max_length=16, choices=SeoPage.PAGE_TYPE_CHOICES)
    anchor_text = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Internal Link Rule"
        verbose_name_plural = "Internal Link Rules"
        indexes = [
            models.Index(fields=["language", "service", "from_page_type"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.language}:{self.service.key}:{self.from_page_type}->{self.to_page_type}"
