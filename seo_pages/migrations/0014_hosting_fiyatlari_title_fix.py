# Fix TR hosting-domain cluster title: web-hosting-fiyatlari → "Web Hosting Fiyatları"
# so Konular shows distinct labels: "Web Hosting Planları" (planlari) vs "Web Hosting Fiyatları" (fiyatlari).

from django.db import migrations


def forward(apps, schema_editor):
    Service = apps.get_model("seo_pages", "Service")
    SeoPage = apps.get_model("seo_pages", "SeoPage")
    svc = Service.objects.filter(key="hosting-domain").first()
    if not svc:
        return
    SeoPage.objects.filter(
        language="tr",
        service=svc,
        page_type="cluster",
        slug="web-hosting-fiyatlari",
    ).update(title="Web Hosting Fiyatları")


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
        slug="web-hosting-fiyatlari",
    ).update(title="Web Hosting Planları")


class Migration(migrations.Migration):
    dependencies = [
        ("seo_pages", "0013_hosting_web_hosting_plans_cluster"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=reverse),
    ]
