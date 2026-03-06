# Align EN SEO clusters with TR: rename seo-for-django-sites -> agency-vs-freelancer,
# add istanbul-seo-agency and seo-friendly-website so TR/EN topics match 1:1.

from django.db import migrations


def _create_cluster_page(SeoPage, Service, slug: str, title: str):
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
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    Service = apps.get_model("seo_pages", "Service")

    # 1) seo-for-django-sites -> agency-vs-freelancer
    updated = SeoPage.objects.filter(
        service__key="seo-services",
        language="en",
        page_type="cluster",
        slug="seo-for-django-sites",
    ).update(slug="agency-vs-freelancer")
    if updated == 0:
        _create_cluster_page(SeoPage, Service, "agency-vs-freelancer", "SEO Agency vs Freelancer")

    # 2) New clusters so EN list matches TR (istanbul-seo-agency, seo-friendly-website)
    _create_cluster_page(SeoPage, Service, "istanbul-seo-agency", "Istanbul SEO Agency")
    _create_cluster_page(SeoPage, Service, "seo-friendly-website", "SEO Friendly Website")


def reverse(apps, schema_editor):
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    # Revert agency-vs-freelancer -> seo-for-django-sites
    SeoPage.objects.filter(
        service__key="seo-services",
        language="en",
        page_type="cluster",
        slug="agency-vs-freelancer",
    ).update(slug="seo-for-django-sites")
    # Remove the two new cluster pages
    SeoPage.objects.filter(
        service__key="seo-services",
        language="en",
        page_type="cluster",
        slug__in=["istanbul-seo-agency", "seo-friendly-website"],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0009_mobile_app_what_is_a_mobile_app_en"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=reverse),
    ]
