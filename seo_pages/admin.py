from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import path
from django.utils import timezone

from .models import InternalLinkRule, SeoPage, Service
from .content.generator_en import generate_en
from .content.generator_tr import generate_tr


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

    actions = ["generate_missing_content", "regenerate_content_force"]

    def _apply_generated(self, page: SeoPage, data: dict):
        page.title = data["title"]
        page.meta_title = data["meta_title"]
        page.meta_description = data["meta_description"]
        page.content_html = data["content_html"]
        page.faq_json = data["faq_json"]
        page.published_at = data.get("published_at") or timezone.now()
        page.is_indexable = True
        page.canonical_url = page.get_absolute_url()
        page.full_clean()
        page.save()

    def _generate_for_page(self, page: SeoPage):
        data = generate_tr(page) if page.language == "tr" else generate_en(page)
        self._apply_generated(page, data)

    @admin.action(description="Generate content for selected (only empty)")
    def generate_missing_content(self, request: HttpRequest, queryset):
        pages = queryset.filter(content_html="")
        n = 0
        for p in pages.select_related("service"):
            self._generate_for_page(p)
            n += 1
        self.message_user(request, f"Generated content for {n} pages.")

    @admin.action(description="Regenerate content for selected (force overwrite)")
    def regenerate_content_force(self, request: HttpRequest, queryset):
        n = 0
        for p in queryset.select_related("service"):
            self._generate_for_page(p)
            n += 1
        self.message_user(request, f"Regenerated content for {n} pages.")

    def get_urls(self):
        urls = super().get_urls()
        my = [
            path("generate-missing-all/", self.admin_site.admin_view(self.generate_missing_all_view), name="seo_pages_generate_missing_all"),
        ]
        return my + urls

    def generate_missing_all_view(self, request: HttpRequest):
        qs = SeoPage.objects.filter(content_html="").select_related("service")
        n = 0
        for p in qs:
            self._generate_for_page(p)
            n += 1
        self.message_user(request, f"Generated content for {n} empty pages.")
        return redirect("..")


@admin.register(InternalLinkRule)
class InternalLinkRuleAdmin(admin.ModelAdmin):
    list_display = ("language", "service", "from_page_type", "to_page_type", "anchor_text")
    list_filter = ("language", "service", "from_page_type", "to_page_type")
    search_fields = ("anchor_text", "service__key")
