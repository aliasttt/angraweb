# Rename EN cluster slug: seo-for-django-sites -> agency-vs-freelancer (SEO Agency vs Freelancer)

from django.db import migrations


def forward(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    updated = SeoPage.objects.filter(
        service__key="seo-services",
        language="en",
        page_type="cluster",
        slug="seo-for-django-sites",
    ).update(slug="agency-vs-freelancer")
    if updated == 0:
        Service = apps.get_model("seo_pages", "Service")
        svc = Service.objects.filter(key="seo-services").first()
        if svc:
            SeoPage.objects.get_or_create(
                language="en",
                service=svc,
                page_type="cluster",
                slug="agency-vs-freelancer",
                defaults={
                    "title": "SEO Agency vs Freelancer",
                    "meta_title": "",
                    "meta_description": "",
                    "canonical_url": f"/en/{svc.en_base_path}/agency-vs-freelancer/",
                    "og_title": "",
                    "og_description": "",
                    "content_html": "",
                    "faq_json": [],
                    "is_indexable": True,
                },
            )


def reverse(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    SeoPage.objects.filter(
        service__key="seo-services",
        language="en",
        page_type="cluster",
        slug="agency-vs-freelancer",
    ).update(slug="seo-for-django-sites")


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0009_mobile_app_what_is_a_mobile_app_en"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=reverse),
    ]
