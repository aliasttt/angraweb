# TR hosting-domain: rename cluster slug django-deployment -> django-yayinlama
# so Turkish URL is /tr/hosting-domain/django-yayinlama/ (not English slug).

from django.db import migrations


def forward(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    svc = Service.objects.filter(key="hosting-domain").first()
    if not svc:
        return
    updated = SeoPage.objects.filter(
        language="tr",
        service=svc,
        page_type="cluster",
        slug="django-deployment",
    ).update(slug="django-yayinlama", canonical_url="/tr/hosting-domain/django-yayinlama/")
    if updated:
        # Ensure canonical_url on all updated rows (update() already set it)
        pass


def reverse(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    svc = Service.objects.filter(key="hosting-domain").first()
    if not svc:
        return
    SeoPage.objects.filter(
        language="tr",
        service=svc,
        page_type="cluster",
        slug="django-yayinlama",
    ).update(slug="django-deployment", canonical_url="/tr/hosting-domain/django-deployment/")


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0011_seo_ensure_istanbul_and_friendly_website_en"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=reverse),
    ]
