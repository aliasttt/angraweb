"""
Cleanup and upgrade all SEO pages: replace link placeholders with HTML,
deduplicate content, add pricing tiers and CTAs, then save.
Runs per language (TR first, then EN); never cross-links languages.
"""
from __future__ import annotations

import re
from typing import List

from django.core.management.base import BaseCommand
from django.conf import settings

from seo_pages.models import SeoPage
from seo_pages.link_placeholder import normalize_placeholders, has_placeholder_syntax


def _replace_placeholders_with_html(page: SeoPage) -> str:
    """Return page.content_html with all link placeholders replaced by <a> tags."""
    from seo_pages.templatetags.seo_pages_tags import _render_content_placeholders
    context = {"request": None}
    return _render_content_placeholders(context, page)


def _dedupe_content(html: str) -> str:
    """Remove consecutive duplicate <p>...</p> blocks."""
    if not html or "<p>" not in html:
        return html
    parts = re.split(r"(<p>.*?</p>)", html, flags=re.DOTALL)
    out: List[str] = []
    prev = None
    for seg in parts:
        if seg.strip().startswith("<p>") and seg.strip().endswith("</p>"):
            if seg == prev:
                continue
            prev = seg
        else:
            prev = None
        out.append(seg)
    return "".join(out)


def _pricing_tiers_html(language: str) -> str:
    """Return 3-tier pricing block (Starter/Standard|Growth/Advanced)."""
    if language == "tr":
        tiers = [
            ("Starter", "Küçük projeler, sınırlı kapsam.", "Temel teslimatlar", "2–4 hafta", "Başlangıç aralığı", "Ek modül, ek tasarım sayfası"),
            ("Standard", "Orta ölçekli kurumsal projeler.", "Kapsamlı teslimatlar, revizyon", "4–8 hafta", "Tipik aralık", "Entegrasyon, özel raporlama"),
            ("Advanced", "Büyük kapsam, entegrasyonlar.", "Tam kapsam, öncelikli destek", "8–14 hafta", "Özel teklif", "Özel geliştirme, SLA"),
        ]
        ideal = "İdeal"
        includes = "Dahil"
        timeline = "Süre"
        range_label = "Aralık"
        addons = "Eklentiler"
    else:
        tiers = [
            ("Starter", "Small scope, limited pages.", "Core deliverables", "2–4 weeks", "From range", "Extra module, extra design page"),
            ("Growth", "Mid-size corporate projects.", "Full deliverables, revisions", "4–8 weeks", "Typical range", "Integrations, custom reporting"),
            ("Advanced", "Large scope, integrations.", "Full scope, priority support", "8–14 weeks", "Custom quote", "Custom development, SLA"),
        ]
        ideal = "Ideal for"
        includes = "Key inclusions"
        timeline = "Timeline"
        range_label = "Range"
        addons = "Add-ons"
    blocks = []
    for name, ideal_text, inc, tl, rng, addon in tiers:
        blocks.append(
            f'<div class="card p-4 mb-3"><h3 class="h5">{name}</h3>'
            f'<p><strong>{ideal}:</strong> {ideal_text}</p>'
            f'<p><strong>{includes}:</strong> {inc}</p>'
            f'<p><strong>{timeline}:</strong> {tl}</p>'
            f'<p><strong>{range_label}:</strong> {rng}</p>'
            f'<p><strong>{addons}:</strong> {addon}</p></div>'
        )
    return "<div class=\"row g-3 mb-4\">" + "".join(blocks) + "</div>"


def _what_affects_price_html(language: str) -> str:
    """What affects price section."""
    if language == "tr":
        title = "Fiyatı neler etkiler?"
        items = [
            "Kapsam (sayfa/ekran, modül sayısı)",
            "Entegrasyonlar (ödeme, CRM/ERP, API'ler)",
            "UI/UX derinliği (şablon uyarlama vs özel tasarım)",
            "Yönetim paneli karmaşıklığı",
            "Performans ve SEO gereksinimleri",
            "Hosting ve bakım dahil mi",
        ]
    else:
        title = "What affects price?"
        items = [
            "Scope (pages/screens, modules)",
            "Integrations (payments, CRM/ERP, APIs)",
            "UI/UX depth (template vs custom design)",
            "Admin panel complexity",
            "Performance and SEO requirements",
            "Hosting and maintenance inclusion",
        ]
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"<h2>{title}</h2><ul>{lis}</ul>"


def _sticky_cta_html(language: str, quote_url: str) -> str:
    """Sticky CTA block with response time promise."""
    if language == "tr":
        cta_text = "Teklif Al"
        promise = "12 saat içinde dönüş"
    else:
        cta_text = "Get a Quote"
        promise = "Reply within 12 hours"
    return (
        f'<div class="card p-4 mt-4 mb-4 seo-cta seo-cta--strong">'
        f'<h3 class="h5">{cta_text}</h3>'
        f'<p class="mb-2">{promise}</p>'
        f'<a class="btn btn-success" href="{quote_url}">{cta_text}</a>'
        f"</div>"
    )


def _trust_badges_html(language: str) -> str:
    """Stack/process/guarantee badges."""
    if language == "tr":
        line = "Django · React Native · Süreç odaklı teslimat · Kapsam netliği taahhüdü"
    else:
        line = "Django · React Native · Process-driven delivery · Scope clarity commitment"
    return f'<p class="small text-muted mb-4">{line}</p>'


def _upgrade_pricing_page_content(page: SeoPage, content: str, quote_url: str) -> str:
    """Prepend tiers, what affects price, sticky CTA and trust to pricing content."""
    lang = page.language
    parts = [
        "<h2>" + ("Paket yaklaşımı" if lang == "tr" else "Package tiers") + "</h2>",
        _pricing_tiers_html(lang),
        _what_affects_price_html(lang),
        _sticky_cta_html(lang, quote_url),
        _trust_badges_html(lang),
        content.strip(),
    ]
    return "\n".join(parts)


class Command(BaseCommand):
    help = "Fix placeholders, dedupe content, upgrade pricing pages and CTAs; save per language (TR then EN)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Do not save; only report changes.")

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        if dry_run:
            self.stdout.write("DRY RUN: no changes will be saved.")

        for language in ("tr", "en"):
            self.stdout.write(f"Processing language: {language}")
            pages = list(
                SeoPage.objects.filter(language=language).select_related("service").order_by("service__key", "page_type", "slug")
            )
            for page in pages:
                changed = False
                content = page.content_html or ""

                # 1) Replace link placeholders with HTML (so DB stores resolved links)
                if has_placeholder_syntax(content):
                    content = _replace_placeholders_with_html(page)
                    changed = True

                # 2) Normalize any remaining placeholder variants to canonical form (if we didn't replace)
                if has_placeholder_syntax(content):
                    content = normalize_placeholders(content)
                    changed = True
                # If still placeholders (e.g. target page missing), skip validation by not saving placeholder content
                if has_placeholder_syntax(content):
                    self.stdout.write(self.style.WARNING(f"  Skip {page}: unreplaced placeholders (missing target pages?)"))
                    continue

                # 3) Dedupe consecutive duplicate paragraphs
                new_content = _dedupe_content(content)
                if new_content != content:
                    content = new_content
                    changed = True

                # 4) Pricing page: add tiers, what affects price, sticky CTA, trust
                if page.page_type == SeoPage.TYPE_PRICING and content:
                    quote_slug = "teklif-al" if language == "tr" else "get-quote"
                    base = page.service.base_path_for_language(language)
                    quote_url = f"/{language}/{base}/{quote_slug}/"
                    content = _upgrade_pricing_page_content(page, content, quote_url)
                    changed = True

                if not changed:
                    continue

                page.content_html = content
                if not dry_run:
                    try:
                        page.save(update_fields=["content_html", "updated_at"])
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  Error saving {page}: {e}"))
                        continue
                self.stdout.write(self.style.SUCCESS(f"  Upgraded: {page}"))

        self.stdout.write("Done.")
