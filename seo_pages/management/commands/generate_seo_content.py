from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from ...content.generator_en import generate_en
from ...content.generator_tr import generate_tr
from ...content.utils import word_count_from_html
from ...models import SeoPage
from ...templatetags.seo_pages_tags import _render_content_placeholders


PLACEHOLDER_RE = re.compile(r"\{\{\s*link:([^\}]+)\s*\}\}")


def _extract_placeholders(html: str) -> List[str]:
    return [m.group(1).strip() for m in PLACEHOLDER_RE.finditer(html or "")]


class Command(BaseCommand):
    help = "Generate SEO silo content for SeoPage entries with empty content_html."

    def add_arguments(self, parser):
        parser.add_argument("--language", choices=["tr", "en", "all"], default="all")
        parser.add_argument("--force", action="store_true", help="Regenerate even if content_html is not empty.")
        parser.add_argument("--service", type=str, default=None, help="Only regenerate pages for this service key (e.g. web-design).")
        parser.add_argument("--page-type", type=str, default=None, help="Only regenerate this page type (e.g. pillar).")
        parser.add_argument("--slug", type=str, default=None, help="Only regenerate pages with this slug (e.g. kurumsal-web-sitesi).")

    @transaction.atomic
    def handle(self, *args, **options):
        lang = options["language"]
        force = options["force"]
        service_key = options.get("service")
        page_type = options.get("page_type")
        slug_filter = options.get("slug")

        qs = SeoPage.objects.select_related("service").order_by("language", "service__key", "page_type", "slug")
        if lang in ("tr", "en"):
            qs = qs.filter(language=lang)
        if service_key:
            qs = qs.filter(service__key=service_key)
        if page_type:
            qs = qs.filter(page_type=page_type)
        if slug_filter is not None:
            qs = qs.filter(slug=slug_filter)
        if not force:
            qs = qs.filter(content_html="")

        pages = list(qs)
        if not pages:
            self.stdout.write("0 pages to generate.")
            return

        now = timezone.now()

        generated = 0
        wc_by_lang_type: Dict[Tuple[str, str], List[int]] = defaultdict(list)
        placeholder_out_counts = Counter()
        inbound_counts = Counter()

        # Precompute URL -> page mapping for broken link checks
        all_pages = list(SeoPage.objects.select_related("service").all())
        url_to_id = {p.get_absolute_url(): p.id for p in all_pages}

        for page in pages:
            if page.language == "tr":
                data = generate_tr(page)
            else:
                data = generate_en(page)

            page.title = data["title"]
            page.meta_title = data["meta_title"]
            page.meta_description = data["meta_description"]
            content_html = data["content_html"]
            # Replace link placeholders with <a> tags so validation (no placeholders in DB) passes
            if PLACEHOLDER_RE.search(content_html):
                page.content_html = content_html
                content_html = _render_content_placeholders({"request": None}, page)
            page.content_html = content_html
            page.faq_json = data["faq_json"]
            page.published_at = data.get("published_at") or now
            page.is_indexable = True
            page.canonical_url = page.get_absolute_url()
            page.full_clean()
            page.save()

            generated += 1
            wc = word_count_from_html(page.content_html)
            wc_by_lang_type[(page.language, page.page_type)].append(wc)

            # Count placeholders from original generated content (before replacement)
            outs = _extract_placeholders(data["content_html"])
            placeholder_out_counts[(page.language, page.page_type)] += len(outs)
            for u in outs:
                inbound_counts[u] += 1

        # Broken link check (placeholders must reference existing pages)
        broken = []
        for u, c in inbound_counts.items():
            if u not in url_to_id:
                broken.append((u, c))

        # Print summary (captured in terminal; user asked not to output content)
        self.stdout.write(f"generated_pages={generated}")

        for (language, page_type), wcs in sorted(wc_by_lang_type.items()):
            if not wcs:
                continue
            avg = sum(wcs) / len(wcs)
            self.stdout.write(f"words_avg language={language} type={page_type} avg={avg:.1f} min={min(wcs)} max={max(wcs)} n={len(wcs)}")

        # Link graph stats (static placeholders only)
        self.stdout.write("placeholder_outgoing_by_lang_type:")
        for k, v in sorted(placeholder_out_counts.items()):
            language, page_type = k
            self.stdout.write(f"  {language}:{page_type} -> {v}")

        # Inbound per cluster (language only, cluster pages)
        for language in (("tr", "en") if lang == "all" else (lang,)):
            cluster_urls = [p.get_absolute_url() for p in all_pages if p.language == language and p.page_type == SeoPage.TYPE_CLUSTER]
            if not cluster_urls:
                continue
            min_in = min(inbound_counts.get(u, 0) for u in cluster_urls)
            avg_in = sum(inbound_counts.get(u, 0) for u in cluster_urls) / len(cluster_urls)
            self.stdout.write(f"inbound_clusters language={language} min={min_in} avg={avg_in:.2f} n={len(cluster_urls)}")

        if broken:
            self.stdout.write(f"broken_placeholder_links={len(broken)}")
            for u, c in broken[:25]:
                self.stdout.write(f"  broken {u} count={c}")
        else:
            self.stdout.write("broken_placeholder_links=0")

