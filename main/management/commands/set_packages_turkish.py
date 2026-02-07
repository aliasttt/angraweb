# -*- coding: utf-8 -*-
"""Set package and package feature titles to Turkish (site is Turkish-only)."""
from django.core.management.base import BaseCommand
from main.models import Package, PackageFeature


# Persian/Arabic/English feature title -> Turkish
FEATURE_TITLE_TR = {
    'طراحی ریسپانسیو': 'Duyarlı tasarım',
    'تا 5 صفحه': '5 sayfaya kadar',
    'تا ۵ صفحه': '5 sayfaya kadar',
    'فرم تماس': 'İletişim formu',
    'سئو پایه': 'Temel SEO',
    'تا 10 صفحه': '10 sayfaya kadar',
    'تا ۱۰ صفحه': '10 sayfaya kadar',
    'پنل ادمین ساده': 'Basit yönetim paneli',
    'دیتابیس پایه': 'Temel veritabanı',
    'صفحات نامحدود': 'Sınırsız sayfa',
    'پنل ادمین اختصاصی': 'Özel yönetim paneli',
    'دیتابیس پیشرفته': 'Gelişmiş veritabanı',
    'طراحی پلتفرم و شبکه اختصاصی': 'Özel platform ve ağ tasarımı',
    'چندین وبسایت و پورتال هماهنگ': 'Birden fazla web sitesi ve portal',
    'چندین وبسایت و پورتال': 'Birden fazla web sitesi ve portal',
    'اپلیکیشن موبایل iOS و Android': 'Android ve iOS mobil uygulama',
    'اپلیکیشن موبایل': 'Mobil uygulama',
    # English fallbacks
    'Responsive design': 'Duyarlı tasarım',
    'Up to 5 pages': '5 sayfaya kadar',
    'Contact form': 'İletişim formu',
    'Basic SEO': 'Temel SEO',
    'Up to 10 pages': '10 sayfaya kadar',
    'Simple admin panel': 'Basit yönetim paneli',
    'Basic database': 'Temel veritabanı',
    'Unlimited pages': 'Sınırsız sayfa',
    'Custom admin panel': 'Özel yönetim paneli',
    'Advanced database': 'Gelişmiş veritabanı',
    'Custom platform design': 'Özel platform ve ağ tasarımı',
    'Multiple sites & portals': 'Birden fazla web sitesi ve portal',
    'iOS & Android app': 'Android ve iOS mobil uygulama',
}

CUSTOM_PRICE_TEXT_TR = "Özel fiyatlandırma için WhatsApp'tan mesaj gönderin"


class Command(BaseCommand):
    help = 'Set package and package feature titles to Turkish for Turkish-only site.'

    def handle(self, *args, **options):
        updated_packages = 0
        updated_features = 0

        # Update custom_price_text for custom package to Turkish
        for p in Package.objects.filter(package_type='custom'):
            if p.custom_price_text:
                p.custom_price_text = CUSTOM_PRICE_TEXT_TR
                p.save(update_fields=['custom_price_text'])
                updated_packages += 1

        # Update PackageFeature titles to Turkish
        for f in PackageFeature.objects.all():
            tr_title = FEATURE_TITLE_TR.get(f.title.strip()) or (FEATURE_TITLE_TR.get((f.title_en or '').strip()) if f.title_en else None)
            if tr_title and f.title != tr_title:
                f.title = tr_title
                f.save(update_fields=['title'])
                updated_features += 1

        self.stdout.write(self.style.SUCCESS(
            f'Updated {updated_packages} package(s), {updated_features} feature(s) to Turkish.'
        ))
