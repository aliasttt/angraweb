from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from django import template
from django.conf import settings

from ..models import SeoPage

register = template.Library()


def _canonical_domain() -> str:
    domain = (getattr(settings, "CANONICAL_DOMAIN", "") or "").strip().rstrip("/")
    if domain.startswith("http://"):
        domain = "https://" + domain[7:]
    return domain


def _abs(request, url_or_path: str) -> str:
    if not url_or_path:
        return ""
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        return url_or_path
    domain = _canonical_domain()
    if domain:
        return domain + url_or_path
    return request.build_absolute_uri(url_or_path) if request else url_or_path


@register.simple_tag(takes_context=True)
def absolute_url(context, url_or_path: str) -> str:
    """
    Turn a model-stored path (e.g. /tr/.../) into an absolute URL using CANONICAL_DOMAIN.
    """
    request = context.get("request")
    return _abs(request, url_or_path)


@register.simple_tag(takes_context=True)
def hreflang_alternates(context, page: SeoPage, mirror_page: Optional[SeoPage] = None) -> List[Dict[str, str]]:
    """
    Returns list of {"lang": "tr|en", "url": "..."} for <link rel="alternate" hreflang="...">.
    """
    request = context.get("request")

    if page.language == "tr":
        tr_page = page
        en_page = mirror_page
    else:
        en_page = page
        tr_page = mirror_page

    alternates: List[Dict[str, str]] = []
    if tr_page:
        alternates.append({"lang": "tr", "url": _abs(request, tr_page.get_absolute_url())})
    if en_page:
        alternates.append({"lang": "en", "url": _abs(request, en_page.get_absolute_url())})
    return alternates


def _jsonld(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


@register.simple_tag(takes_context=True)
def jsonld_breadcrumbs(context, page: SeoPage) -> str:
    request = context.get("request")
    domain = _canonical_domain() or (request.build_absolute_uri("/")[:-1] if request else "")

    home_url = f"{domain}/{page.language}/"
    service_pillar_url = f"{domain}/{page.language}/{page.service.base_path_for_language(page.language)}/"

    items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
        {
            "@type": "ListItem",
            "position": 2,
            "name": page.service.name_for_language(page.language),
            "item": service_pillar_url,
        },
    ]

    if page.page_type != SeoPage.TYPE_PILLAR:
        items.append(
            {
                "@type": "ListItem",
                "position": 3,
                "name": page.title,
                "item": f"{domain}{page.get_absolute_url()}",
            }
        )

    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return _jsonld(data)


@register.simple_tag(takes_context=True)
def jsonld_primary(context, page: SeoPage) -> str:
    request = context.get("request")
    domain = _canonical_domain() or (request.build_absolute_uri("/")[:-1] if request else "")
    url = f"{domain}{page.get_absolute_url()}"

    if page.page_type in (SeoPage.TYPE_GUIDE, SeoPage.TYPE_CLUSTER):
        data: Dict[str, Any] = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page.meta_title or page.title,
            "description": page.meta_description or "",
            "inLanguage": page.language,
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        }
        return _jsonld(data)

    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": page.meta_title or page.title,
        "description": page.meta_description or "",
        "inLanguage": page.language,
        "url": url,
        "provider": {"@type": "Organization", "name": "Angraweb"},
    }
    return _jsonld(data)


@register.simple_tag
def jsonld_faq(page: SeoPage) -> str:
    if not page.faq_json:
        return ""
    main_entity = []
    for item in page.faq_json:
        q = (item or {}).get("question", "")
        a = (item or {}).get("answer", "")
        if not q or not a:
            continue
        main_entity.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    if not main_entity:
        return ""
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main_entity}
    return _jsonld(data)

