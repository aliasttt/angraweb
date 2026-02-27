from __future__ import annotations

import html
import json
import random
import re
from typing import Any, Dict, List, Optional

from django import template
from django.conf import settings
from django.db.models import Q
from django.utils.safestring import mark_safe

from ..models import SeoPage
from ..link_placeholder import PLACEHOLDER_PATTERN as _PLACEHOLDER_RE
from ..silo_config import SERVICE_SILO_MAP

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


@register.simple_tag
def silo_url(language: str, service_key: str, page_type: str = "pillar", slug: str = "") -> str:
    """
    Return language-safe service silo URL paths.
    - language: tr|en
    - service_key: one of SERVICE_SILO_MAP keys (e.g. web-design)
    - page_type: pillar|pricing|guide|quote|cluster
    - slug: cluster slug if page_type=cluster
    """
    if language not in ("tr", "en"):
        language = "tr"
    cfg = SERVICE_SILO_MAP.get(service_key, {}).get(language)
    if not cfg:
        return f"/{language}/"
    base = cfg["base_path"]
    if page_type == "pillar":
        return f"/{language}/{base}/"
    if page_type == "pricing":
        return f"/{language}/{base}/{'fiyatlar' if language=='tr' else 'pricing'}/"
    if page_type == "guide":
        return f"/{language}/{base}/{'rehber' if language=='tr' else 'guide'}/"
    if page_type == "quote":
        return f"/{language}/{base}/{'teklif-al' if language=='tr' else 'get-quote'}/"
    if page_type == "cluster" and slug:
        return f"/{language}/{base}/{slug}/"
    return f"/{language}/{base}/"


@register.simple_tag
def silo_pillar_for_service_type(language: str, service_type: str) -> str:
    """
    Map `main.Service.service_type` to the new silo pillar URLs.
    """
    mapping = {
        "web_design": "web-design",
        "mobile_app": "mobile-app-development",
        "ecommerce": "ecommerce-development",
        "seo": "seo-services",
        "hosting": "hosting-domain",
        "ui_ux": "ui-ux-design",
    }
    key = mapping.get(service_type or "")
    if not key:
        return f"/{language or 'tr'}/"
    return silo_url(language, key, "pillar")


def _is_same_language(page: SeoPage, url: str) -> bool:
    return url.startswith(f"/{page.language}/")


def _resolve_target_page(url: str) -> Optional[SeoPage]:
    # canonical_url is stored as path for seo_pages
    return SeoPage.objects.select_related("service").filter(Q(canonical_url=url) | Q(canonical_url=url.rstrip("/"))).first()


def _slug_words_from_url(url: str) -> List[str]:
    parts = [p for p in (url or "").strip("/").split("/") if p]
    if len(parts) < 3:
        return []
    slug = parts[-1]
    if slug in ("fiyatlar", "rehber", "teklif-al", "pricing", "guide", "get-quote"):
        return []
    return [w for w in slug.replace("-", " ").split() if w]


def _choose_anchor(page: SeoPage, target: SeoPage, url: str, mode: str) -> str:
    """
    mode: partial | semantic | branded
    Rules are driven by SOURCE page_type.
    """
    lang = page.language
    if page.page_type == SeoPage.TYPE_QUOTE:
        return "Teklif Al" if lang == "tr" else "Get a Quote"

    if page.page_type == SeoPage.TYPE_PRICING:
        if lang == "tr":
            options = {
                "semantic": ["fiyat detaylarını inceleyin", "paketleri karşılaştırın", "maliyet kalemlerini görün", "fiyatlandırmayı okuyun"],
                "partial": ["fiyatlar", "fiyatlandırma", "paket fiyatları"],
                "branded": ["Angraweb fiyatlandırma", "Angraweb paketleri"],
            }
        else:
            options = {
                "semantic": ["see pricing details", "compare pricing options", "review cost drivers", "read pricing"],
                "partial": ["pricing", "pricing options", "cost"],
                "branded": ["Angraweb pricing", "Angraweb pricing options"],
            }
        return random.choice(options.get(mode, options["semantic"]))

    if page.page_type == SeoPage.TYPE_GUIDE:
        if lang == "tr":
            options = {
                "semantic": ["detaylı rehberi okuyun", "adım adım süreci inceleyin", "kontrol listesini görün", "rehber bölümüne göz atın"],
                "partial": ["rehber", "adım adım süreç", "uygulama rehberi"],
                "branded": ["Angraweb rehberi", "Angraweb süreç rehberi"],
            }
        else:
            options = {
                "semantic": ["read the guide", "follow the step-by-step workflow", "see the checklist", "review the guide section"],
                "partial": ["guide", "step-by-step guide", "implementation guide"],
                "branded": ["Angraweb guide", "Angraweb workflow guide"],
            }
        return random.choice(options.get(mode, options["semantic"]))

    # Cluster / Pillar sources: partial match anchors should resemble target topic
    if mode == "branded":
        return "Angraweb"

    if mode == "partial":
        words = _slug_words_from_url(url)
        if page.language == "tr":
            if words:
                return " ".join(words[:3])
            return target.title
        if words:
            return " ".join(words[:3]).lower()
        return target.title

    # semantic
    if page.language == "tr":
        return random.choice(
            [
                "detayları inceleyin",
                "konuyu adım adım okuyun",
                "ilgili sayfaya geçin",
                "kapsamı ve yaklaşımı görün",
            ]
        )
    return random.choice(
        [
            "read the details",
            "see the related page",
            "review the approach",
            "explore the topic",
        ]
    )


def _assign_anchor_modes(n: int, seed: str) -> List[str]:
    """
    Anchor distribution:
    - 10–20% partial
    - 60–70% semantic
    - 10–20% branded
    """
    if n <= 0:
        return []
    rnd = random.Random(seed)
    partial_n = max(1, round(n * rnd.uniform(0.10, 0.20)))
    branded_n = max(1, round(n * rnd.uniform(0.10, 0.20)))
    semantic_n = max(0, n - partial_n - branded_n)
    modes = (["partial"] * partial_n) + (["branded"] * branded_n) + (["semantic"] * semantic_n)
    rnd.shuffle(modes)
    return modes[:n]


def _related_reading_html(page: SeoPage, seed: str) -> str:
    qs = SeoPage.objects.filter(language=page.language, service=page.service, is_indexable=True, published_at__isnull=False)
    clusters = list(qs.filter(page_type=SeoPage.TYPE_CLUSTER).exclude(id=page.id).only("id", "title", "canonical_url", "slug"))
    if not clusters:
        return ""

    # Weighted by "type similarity": clusters for cluster/guide/pillar, cost-ish clusters for pricing, high-intent clusters for quote.
    def is_cost(p: SeoPage) -> bool:
        return any(k in (p.slug or "") for k in ["fiyat", "maliyet", "cost", "pricing"])

    rnd = random.Random(seed + ":related")
    pool = clusters
    if page.page_type == SeoPage.TYPE_PRICING:
        cost_pool = [c for c in clusters if is_cost(c)]
        pool = cost_pool or clusters
    elif page.page_type == SeoPage.TYPE_QUOTE:
        # "high intent" cluster heuristic: comparison or hiring words
        hi = [c for c in clusters if any(k in (c.slug or "") for k in ["vs", "hire", "freelancer", "ajans", "company", "istanbul"])]
        pool = hi or clusters

    rnd.shuffle(pool)
    pick = pool[:3]
    if not pick:
        return ""

    heading = "İlgili Okumalar" if page.language == "tr" else "Related Reading"
    items = "".join(
        f"<li><a class=\"inline-link\" href=\"{html.escape(p.get_absolute_url())}\">{html.escape(p.title)}</a></li>"
        for p in pick
    )
    return (
        "<div class=\"card p-4 mt-4 seo-related-reading\">"
        f"<h2 class=\"h5 mb-3\">{html.escape(heading)}</h2>"
        f"<ul class=\"mb-0\">{items}</ul>"
        "</div>"
    )


def _render_content_placeholders(context: dict, page: SeoPage) -> str:
    """Replace link placeholders in page.content_html with <a class=\"inline-link\">. Returns raw string."""
    src_html = page.content_html or ""
    if not src_html:
        return ""

    request = context.get("request")
    domain = _canonical_domain()
    placeholders = list(_PLACEHOLDER_RE.finditer(src_html))
    modes = _assign_anchor_modes(len(placeholders), seed=f"{page.language}:{page.id}:{page.page_type}")

    out = []
    last = 0
    for i, m in enumerate(placeholders):
        out.append(src_html[last : m.start()])
        url = (m.group(1) or "").strip()

        if not _is_same_language(page, url):
            out.append(html.escape(url))
            last = m.end()
            continue

        target = _resolve_target_page(url)
        if not target:
            out.append(html.escape(url))
            last = m.end()
            continue

        mode = modes[i] if i < len(modes) else "semantic"
        anchor = _choose_anchor(page, target, url, mode)
        href = url if url.startswith("/") else ((domain + url) if domain else (request.build_absolute_uri(url) if request else url))
        out.append(f"<a class=\"inline-link\" href=\"{html.escape(href)}\">{html.escape(anchor)}</a>")
        last = m.end()

    out.append(src_html[last:])
    return "".join(out)


@register.simple_tag(takes_context=True)
def render_internal_links(context, page: SeoPage) -> str:
    """
    Parses link placeholders (e.g. {{ link:/tr/.../ }}, { link:/en/.../ }) and replaces
    them with safe <a class="inline-link"> tags. Also appends a related reading block.
    """
    html_part = _render_content_placeholders(context, page)
    if not html_part:
        return ""
    related = _related_reading_html(page, seed=f"{page.language}:{page.id}:{page.page_type}")
    if related:
        html_part += related
    return mark_safe(html_part)


@register.simple_tag(takes_context=True)
def render_content(context, page: SeoPage) -> str:
    """
    Returns safe HTML with link placeholders replaced by <a class="inline-link"> anchors.
    Use this when you only need the main content without the related reading block.
    """
    return mark_safe(_render_content_placeholders(context, page))

