# Add new cluster pages for web-design silo (professional-web-design, web-developer-istanbul EN + web-tasarim-nedir, web-sitesi-nasil-yapilir TR)

from django.db import migrations
from django.utils import timezone


def _title_from_slug(slug: str) -> str:
    if not slug:
        return ""
    return slug.replace("-", " ").replace("  ", " ").title()


def add_new_cluster_pages(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")

    svc = Service.objects.filter(key="web-design").first()
    if not svc:
        return

    now = timezone.now()
    new_pages = [
        ("tr", "web-tasarim-nedir"),
        ("tr", "web-sitesi-nasil-yapilir"),
        ("en", "professional-web-design"),
        ("en", "web-developer-istanbul"),
    ]
    for language, slug in new_pages:
        base = svc.tr_base_path if language == "tr" else svc.en_base_path
        url = f"/{language}/{base}/{slug}/"
        SeoPage.objects.get_or_create(
            language=language,
            service=svc,
            page_type="cluster",
            slug=slug,
            defaults={
                "title": _title_from_slug(slug),
                "meta_title": "",
                "meta_description": "",
                "canonical_url": url,
                "og_title": "",
                "og_description": "",
                "content_html": "",
                "faq_json": [],
                "is_indexable": True,
                "published_at": now,
            },
        )


def remove_new_cluster_pages(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    slugs = [
        "web-tasarim-nedir",
        "web-sitesi-nasil-yapilir",
        "professional-web-design",
        "web-developer-istanbul",
    ]
    SeoPage.objects.filter(
        service__key="web-design",
        page_type="cluster",
        slug__in=slugs,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0003_alter_seopage_canonical_url"),
    ]

    operations = [
        migrations.RunPython(add_new_cluster_pages, reverse_code=remove_new_cluster_pages),
    ]
