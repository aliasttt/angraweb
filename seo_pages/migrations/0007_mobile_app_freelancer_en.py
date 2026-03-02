# Add EN cluster page: mobile-app-freelancer (Working with a Mobile App Freelancer)

from django.db import migrations
from django.utils import timezone


def _title_from_slug(slug: str) -> str:
    if not slug:
        return ""
    return slug.replace("-", " ").replace("  ", " ").title()


def add_mobile_app_freelancer_page(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")

    svc = Service.objects.filter(key="mobile-app-development").first()
    if not svc:
        return

    base = svc.en_base_path
    url = f"/en/{base}/mobile-app-freelancer/"
    SeoPage.objects.get_or_create(
        language="en",
        service=svc,
        page_type="cluster",
        slug="mobile-app-freelancer",
        defaults={
            "title": _title_from_slug("mobile-app-freelancer"),
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


def remove_mobile_app_freelancer_page(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    SeoPage.objects.filter(
        service__key="mobile-app-development",
        language="en",
        page_type="cluster",
        slug="mobile-app-freelancer",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0006_mobile_app_istanbul_service_en"),
    ]

    operations = [
        migrations.RunPython(add_mobile_app_freelancer_page, reverse_code=remove_mobile_app_freelancer_page),
    ]
