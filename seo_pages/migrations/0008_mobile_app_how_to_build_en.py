# Add EN cluster page: how-to-build-a-mobile-app (How to Build a Mobile App)

from django.db import migrations
from django.utils import timezone


def _title_from_slug(slug: str) -> str:
    if not slug:
        return ""
    return slug.replace("-", " ").replace("  ", " ").title()


def add_how_to_build_mobile_app_page(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")

    svc = Service.objects.filter(key="mobile-app-development").first()
    if not svc:
        return

    base = svc.en_base_path
    url = f"/en/{base}/how-to-build-a-mobile-app/"
    SeoPage.objects.get_or_create(
        language="en",
        service=svc,
        page_type="cluster",
        slug="how-to-build-a-mobile-app",
        defaults={
            "title": _title_from_slug("how-to-build-a-mobile-app"),
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


def remove_how_to_build_mobile_app_page(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    SeoPage.objects.filter(
        service__key="mobile-app-development",
        language="en",
        page_type="cluster",
        slug="how-to-build-a-mobile-app",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0007_mobile_app_freelancer_en"),
    ]

    operations = [
        migrations.RunPython(add_how_to_build_mobile_app_page, reverse_code=remove_how_to_build_mobile_app_page),
    ]
