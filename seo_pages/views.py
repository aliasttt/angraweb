from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.utils import translation

from .models import SeoPage, Service
from .silo_config import get_mirrored_slug, get_service_bases


def _get_service_for_base(language: str, service_base: str) -> Service:
    if language == "tr":
        svc = Service.objects.filter(tr_base_path=service_base).first()
    elif language == "en":
        svc = Service.objects.filter(en_base_path=service_base).first()
    else:
        svc = None
    if not svc:
        raise Http404("Service not found")
    return svc


def _get_page(language: str, service: Service, page_type: str, slug: str) -> SeoPage:
    return SeoPage.objects.select_related("service").filter(
        language=language,
        service=service,
        page_type=page_type,
        slug=slug,
    ).first()


def seo_page_view(request, language: str, service_base: str, page_type: str, slug: str):
    """
    Render a SeoPage by (language, service_base_path, page_type, slug).

    Language is explicit (/tr/..., /en/...) to avoid invalid mixed slug routes.
    """

    if language not in ("tr", "en"):
        raise Http404("Invalid language")

    translation.activate(language)
    request.LANGUAGE_CODE = language

    service = _get_service_for_base(language, service_base)
    service_name = service.tr_name if language == "tr" else service.en_name
    service_base_path = service.tr_base_path if language == "tr" else service.en_base_path
    page = _get_page(language, service, page_type, slug)
    if not page:
        raise Http404("Page not found")

    # Internal linking graph (language-only).
    pillar = _get_page(language, service, SeoPage.TYPE_PILLAR, "")
    pricing = _get_page(language, service, SeoPage.TYPE_PRICING, "fiyatlar" if language == "tr" else "pricing")
    guide = _get_page(language, service, SeoPage.TYPE_GUIDE, "rehber" if language == "tr" else "guide")
    quote = _get_page(language, service, SeoPage.TYPE_QUOTE, "teklif-al" if language == "tr" else "get-quote")
    clusters = list(
        SeoPage.objects.filter(language=language, service=service, page_type=SeoPage.TYPE_CLUSTER)
        .order_by("slug")
        .only("id", "language", "page_type", "slug", "title", "service_id")
    )

    related_reading = []
    if page.page_type == SeoPage.TYPE_GUIDE:
        related_reading = clusters[:10]
    elif page.page_type == SeoPage.TYPE_PRICING:
        related_reading = clusters[:6]
    elif page.page_type == SeoPage.TYPE_CLUSTER:
        related_reading = [c for c in clusters if c.id != page.id][:6]
    elif page.page_type == SeoPage.TYPE_PILLAR:
        related_reading = clusters[:12]

    # hreflang alternates via strict mirrored slug mapping (never "swap prefix and keep path").
    other_lang = "en" if language == "tr" else "tr"
    mirror_service_base = service.base_path_for_language(other_lang)
    mirror_slug = get_mirrored_slug(service.key, page.page_type, language, page.slug)
    mirror_page = None
    if mirror_slug is not None:
        mirror_page = _get_page(other_lang, service, page.page_type, mirror_slug)

    nav_services = list(Service.objects.order_by("key").only("id", "key", "tr_name", "en_name", "tr_base_path", "en_base_path"))
    current_service_bases = get_service_bases(language)

    context = {
        "page": page,
        "service": service,
        "service_name": service_name,
        "service_base_path": service_base_path,
        "language": language,
        "pillar": pillar,
        "pricing": pricing,
        "guide": guide,
        "quote": quote,
        "clusters": clusters,
        "related_reading": related_reading,
        "nav_services": nav_services,
        "service_bases": current_service_bases,
        "mirror_page": mirror_page,
        "mirror_language": other_lang,
        "mirror_service_base": mirror_service_base,
    }

    template_map = {
        SeoPage.TYPE_PILLAR: "seo_pages/pillar.html",
        SeoPage.TYPE_PRICING: "seo_pages/pricing.html",
        SeoPage.TYPE_GUIDE: "seo_pages/guide.html",
        SeoPage.TYPE_CLUSTER: "seo_pages/cluster.html",
        SeoPage.TYPE_QUOTE: "seo_pages/quote.html",
    }
    tpl = template_map.get(page.page_type)
    if not tpl:
        raise Http404("Unknown page type")
    return render(request, tpl, context)
