# Add EN cluster page: istanbul-service (Mobile App Development in Istanbul)

from django.db import migrations
from django.utils import timezone


def _title_from_slug(slug: str) -> str:
    if not slug:
        return ""
    return slug.replace("-", " ").replace("  ", " ").title()


def add_istanbul_service_page(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")

    svc = Service.objects.filter(key="mobile-app-development").first()
    if not svc:
        return

    base = svc.en_base_path
    url = f"/en/{base}/istanbul-service/"
    SeoPage.objects.get_or_create(
        language="en",
        service=svc,
        page_type="cluster",
        slug="istanbul-service",
        defaults={
            "title": _title_from_slug("istanbul-service"),
            "meta_title": "",
            "meta_description": "",
            "canonical_url": url,
            "og_title": "",
            "og_description": "",
            "content_html": "",
            "faq_json": [],
            "is_indexable": True,
            "published_at": timezone.now(),
        },
    )


def remove_istanbul_service_page(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    SeoPage.objects.filter(
        service__key="mobile-app-development",
        language="en",
        page_type="cluster",
        slug="istanbul-service",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0005_mobile_app_android_or_ios_en"),
    ]

    operations = [
        migrations.RunPython(add_istanbul_service_page, reverse_code=remove_istanbul_service_page),
    ]
