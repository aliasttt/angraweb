"""
Audit sitemap (or internal links) for meta: title, description, h1, canonical, status.
Usage: python manage.py insights_audit_meta --sitemap https://example.com/sitemap.xml --max-pages 200
"""
import re
import time
import logging
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from insights.models import MetaAuditResult

logger = logging.getLogger(__name__)

USER_AGENT = 'AngrawebInsightsAudit/1.0'
TITLE_MIN, TITLE_MAX = 30, 60
DESC_MIN, DESC_MAX = 70, 160


def fetch_urls_from_sitemap(sitemap_url: str, max_urls: int = 200) -> list:
    """Parse sitemap XML and return list of URLs (index or urlset)."""
    try:
        r = requests.get(sitemap_url, timeout=15, headers={'User-Agent': USER_AGENT})
        r.raise_for_status()
    except Exception as e:
        logger.warning('Sitemap fetch failed: %s', e)
        return []
    urls = []
    try:
        root = ET.fromstring(r.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for loc in root.findall('.//sm:url/sm:loc', ns):
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
                if len(urls) >= max_urls:
                    break
        if not urls:
            for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                if loc is not None and loc.text:
                    urls.append(loc.text.strip())
                    if len(urls) >= max_urls:
                        break
    except ET.ParseError:
        pass
    return urls


def extract_meta(html: str, url: str) -> dict:
    """Extract title, meta description, h1 count, canonical from HTML."""
    title = ''
    desc = ''
    canonical = ''
    h1_count = 0
    m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I | re.DOTALL)
    if m:
        title = re.sub(r'\s+', ' ', m.group(1).strip())[:255]
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.I)
    if m:
        desc = re.sub(r'\s+', ' ', m.group(1).strip())[:500]
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', html, re.I)
    if m:
        canonical = urljoin(url, m.group(1).strip())[:2048]
    h1_count = len(re.findall(r'<h1[^>]*>', html, re.I))
    return {'title': title, 'description': desc, 'canonical': canonical, 'h1_count': h1_count}


def build_issues(title: str, description: str, h1_count: int) -> list:
    """Build list of SEO issues."""
    issues = []
    if not title:
        issues.append('missing_title')
    elif len(title) < TITLE_MIN:
        issues.append(f'title_too_short_{len(title)}')
    elif len(title) > TITLE_MAX:
        issues.append(f'title_too_long_{len(title)}')
    if not description:
        issues.append('missing_description')
    elif len(description) < DESC_MIN:
        issues.append(f'description_too_short_{len(description)}')
    elif len(description) > DESC_MAX:
        issues.append(f'description_too_long_{len(description)}')
    if h1_count == 0:
        issues.append('no_h1')
    elif h1_count > 1:
        issues.append(f'multiple_h1_{h1_count}')
    return issues


class Command(BaseCommand):
    help = 'Audit sitemap URLs for meta (title, description, h1, canonical, status)'

    def add_arguments(self, parser):
        parser.add_argument('--sitemap', type=str, default='', help='Sitemap URL')
        parser.add_argument('--max-pages', type=int, default=200, help='Max URLs to check')

    def handle(self, *args, **options):
        sitemap_url = (options.get('sitemap') or '').strip()
        max_pages = options.get('max_pages') or 200
        if not sitemap_url:
            self.stdout.write(self.style.WARNING('Provide --sitemap URL.'))
            return
        urls = fetch_urls_from_sitemap(sitemap_url, max_urls=max_pages)
        if not urls:
            self.stdout.write(self.style.WARNING('No URLs found in sitemap.'))
            return
        self.stdout.write(f'Auditing {len(urls)} URLs...')
        for url in urls:
            try:
                t0 = time.perf_counter()
                r = requests.get(url, timeout=10, headers={'User-Agent': USER_AGENT}, allow_redirects=True)
                resp_ms = int((time.perf_counter() - t0) * 1000)
                meta = extract_meta(r.text, url)
                issues = build_issues(meta['title'], meta['description'], meta['h1_count'])
                MetaAuditResult.objects.create(
                    url=url,
                    checked_at=timezone.now(),
                    title=meta['title'],
                    description=meta['description'],
                    h1_count=meta['h1_count'],
                    canonical=meta['canonical'],
                    status_code=r.status_code,
                    resp_ms=resp_ms,
                    issues_json=issues,
                )
            except Exception as e:
                logger.warning('Audit failed for %s: %s', url, e)
                MetaAuditResult.objects.create(url=url, checked_at=timezone.now(), issues_json=['fetch_error'])
        self.stdout.write(self.style.SUCCESS(f'Audit done: {len(urls)} URLs'))
