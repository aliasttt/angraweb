# Create hosting-domain cluster pages: web-hosting-planlari (TR), web-hosting-plans (EN).

from django.db import migrations


def _get_or_create_cluster(apps, language: str, slug: str, title: str):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    svc = Service.objects.filter(key="hosting-domain").first()
    if not svc:
        return
    base = svc.tr_base_path if language == "tr" else svc.en_base_path
    canonical_url = f"/{language}/{base}/{slug}/"
    SeoPage.objects.get_or_create(
        language=language,
        service=svc,
        page_type="cluster",
        slug=slug,
        defaults={
            "title": title,
            "meta_title": "",
            "meta_description": "",
            "canonical_url": canonical_url,
            "og_title": "",
            "og_description": "",
            "content_html": "",
            "faq_json": [],
            "is_indexable": True,
        },
    )


def forward(apps, schema_editor):
    _get_or_create_cluster(apps, "tr", "web-hosting-planlari", "Web Hosting Planları")
    _get_or_create_cluster(apps, "en", "web-hosting-plans", "Web Hosting Plans")


def reverse(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    SeoPage.objects.filter(
        service__key="hosting-domain",
        page_type="cluster",
        slug__in=["web-hosting-planlari", "web-hosting-plans"],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0012_tr_django_yayinlama_slug"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=reverse),
    ]
