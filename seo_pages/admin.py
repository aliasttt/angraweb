from django.contrib import admin

from .models import InternalLinkRule, SeoPage, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("key", "tr_base_path", "en_base_path", "tr_name", "en_name")
    search_fields = ("key", "tr_name", "en_name", "tr_base_path", "en_base_path")
    ordering = ("key",)


@admin.register(SeoPage)
class SeoPageAdmin(admin.ModelAdmin):
    list_display = (
        "language",
        "service",
        "page_type",
        "slug",
        "is_indexable",
        "published_at",
        "updated_at",
    )
    list_filter = ("language", "page_type", "is_indexable", "service")
    search_fields = ("title", "meta_title", "meta_description", "slug", "service__key")
    ordering = ("language", "service__key", "page_type", "slug")
    date_hierarchy = "published_at"

    fieldsets = (
        (None, {"fields": ("language", "service", "page_type", "slug")}),
        ("SEO", {"fields": ("title", "meta_title", "meta_description", "canonical_url", "og_title", "og_description")}),
        ("Content", {"fields": ("content_html", "faq_json")}),
        ("Publishing", {"fields": ("is_indexable", "published_at")}),
    )


@admin.register(InternalLinkRule)
class InternalLinkRuleAdmin(admin.ModelAdmin):
    list_display = ("language", "service", "from_page_type", "to_page_type", "anchor_text")
    list_filter = ("language", "service", "from_page_type", "to_page_type")
    search_fields = ("anchor_text", "service__key")
