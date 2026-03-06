# Ensure EN cluster pages istanbul-seo-agency and seo-friendly-website exist
# so they appear in the English Topics list (aligned with TR Konular).

from django.db import migrations


def _get_or_create_cluster(apps, slug: str, title: str):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    svc = Service.objects.filter(key="seo-services").first()
    if not svc:
        return
    SeoPage.objects.get_or_create(
        language="en",
        service=svc,
        page_type="cluster",
        slug=slug,
        defaults={
            "title": title,
            "meta_title": "",
            "meta_description": "",
            "canonical_url": f"/en/{svc.en_base_path}/{slug}/",
            "og_title": "",
            "og_description": "",
            "content_html": "",
            "faq_json": [],
            "is_indexable": True,
        },
    )


def forward(apps, schema_editor):
    _get_or_create_cluster(apps, "istanbul-seo-agency", "Istanbul SEO Agency")
    _get_or_create_cluster(apps, "seo-friendly-website", "SEO Friendly Website")


def reverse(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    SeoPage.objects.filter(
        service__key="seo-services",
        language="en",
        page_type="cluster",
        slug__in=["istanbul-seo-agency", "seo-friendly-website"],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0010_seo_agency_vs_freelancer_cluster"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=reverse),
    ]
