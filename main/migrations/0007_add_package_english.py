# Data migration: set English titles for Package and PackageFeature

from django.db import migrations


# English titles for packages by package_type
PACKAGE_TITLE_EN = {
    'basic': 'Basic Package',
    'commercial': 'Commercial Package',
    'professional': 'Professional Package',
    'custom': 'Custom Package',
}

# English feature titles per package_type (by order)
FEATURES_EN = {
    'basic': [
        'Responsive Design',
        'Up to 5 pages',
        'Contact Form',
        'Basic SEO',
    ],
    'commercial': [
        'Responsive Design',
        'Up to 10 pages',
        'Simple Admin Panel',
        'Basic Database',
    ],
    'professional': [
        'Responsive Design',
        'Unlimited Pages',
        'Dedicated Admin Panel',
        'Advanced Database',
    ],
    'custom': [
        'Dedicated Platform & Network Design',
        'Multiple Websites & Harmonized Portals',
        'Android and iOS Mobile Applications',
    ],
}


def set_package_english(apps, schema_editor):
    Package = apps.get_model('main', 'Package')
    PackageFeature = apps.get_model('main', 'PackageFeature')

    for package in Package.objects.filter(active=True):
        en_title = PACKAGE_TITLE_EN.get(package.package_type)
        if en_title:
            package.title_en = en_title
            package.save(update_fields=['title_en'])

        if package.package_type == 'custom':
            package.description_en = 'Send a message via WhatsApp for custom pricing.'
            package.save(update_fields=['description_en'])

        feature_titles = FEATURES_EN.get(package.package_type, [])
        features = list(PackageFeature.objects.filter(package=package).order_by('order'))
        for i, feature in enumerate(features):
            if i < len(feature_titles):
                feature.title_en = feature_titles[i]
                feature.save(update_fields=['title_en'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_add_sample_testimonials'),
    ]

    operations = [
        migrations.RunPython(set_package_english, noop_reverse),
    ]
