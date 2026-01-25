from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import Service, Package, PackageFeature, Project, ProjectVideo
import sys
import shutil
from pathlib import Path


class Command(BaseCommand):
    help = 'Create initial data for services, packages, projects and video demos'

    def handle(self, *args, **options):
        # Fix encoding for Windows console
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        # ایجاد خدمات
        services_data = [
            {
                'title': 'Uzman Web Tasarımı',
                'service_type': 'web_design',
                'description': 'İşinizi büyütecek modern ve hızlı web siteleri tasarlıyorum.',
                'icon': 'fas fa-code',
                'order': 1,
                'featured': True,
            },
            {
                'title': 'E-Ticaret Çözümleri',
                'service_type': 'ecommerce',
                'description': 'Satışlarınızı artıracak profesyonel e-ticaret sitesi.',
                'icon': 'fas fa-shopping-cart',
                'order': 2,
                'featured': True,
            },
            {
                'title': 'Mobil Uyumlu Tasarım',
                'service_type': 'web_design',
                'description': 'Tüm cihazlarda mükemmel görünen web siteleri.',
                'icon': 'fas fa-mobile-alt',
                'order': 3,
            },
            {
                'title': 'Hosting ve Yayınlama',
                'service_type': 'hosting',
                'description': 'Web sitenizi güvenli sunucularda yayınlıyorum.',
                'icon': 'fas fa-server',
                'order': 4,
            },
            {
                'title': 'Kullanıcı Deneyimi Tasarımı',
                'service_type': 'ui_ux',
                'description': 'Müşterilerinizi etkileyecek güzel ve kullanışlı arayüz tasarımları.',
                'icon': 'fas fa-paint-brush',
                'order': 5,
            },
            {
                'title': 'Hız ve SEO',
                'service_type': 'seo',
                'description': 'Web sitenizi Google\'da üst sıralara çıkarıyorum.',
                'icon': 'fas fa-cogs',
                'order': 6,
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                try:
                    self.stdout.write(self.style.SUCCESS(f'Service created: {service.title}'))
                except:
                    pass
        
        # ایجاد پکیج‌ها
        packages_data = [
            {
                'title': 'پکیج پایه',
                'package_type': 'basic',
                'price': 5000,
                'currency': 'TL',
                'order': 1,
            },
            {
                'title': 'پکیج تجاری',
                'package_type': 'commercial',
                'price': 10000,
                'currency': 'TL',
                'order': 2,
                'popular': True,
            },
            {
                'title': 'پکیج حرفه‌ای',
                'package_type': 'professional',
                'price': 15000,
                'currency': 'TL',
                'order': 3,
            },
            {
                'title': 'پکیج کاستوم',
                'package_type': 'custom',
                'price': 0,
                'custom_price_text': 'برای قیمت‌گذاری اختصاصی واتساپ پیام دهید',
                'order': 4,
            },
        ]
        
        for package_data in packages_data:
            package, created = Package.objects.get_or_create(
                title=package_data['title'],
                defaults=package_data
            )
            if created:
                try:
                    self.stdout.write(self.style.SUCCESS(f'Package created: {package.title}'))
                except:
                    pass
                
                # اضافه کردن ویژگی‌های پیش‌فرض
                if package.package_type == 'basic':
                    features = [
                        'طراحی ریسپانسیو',
                        'تا 5 صفحه',
                        'فرم تماس',
                        'سئو پایه',
                    ]
                elif package.package_type == 'commercial':
                    features = [
                        'طراحی ریسپانسیو',
                        'تا 10 صفحه',
                        'پنل ادمین ساده',
                        'دیتابیس پایه',
                    ]
                elif package.package_type == 'professional':
                    features = [
                        'طراحی ریسپانسیو',
                        'صفحات نامحدود',
                        'پنل ادمین اختصاصی',
                        'دیتابیس پیشرفته',
                    ]
                else:
                    features = [
                        'طراحی پلتفرم و شبکه اختصاصی',
                        'چندین وبسایت و پورتال هماهنگ',
                        'اپلیکیشن موبایل iOS و Android',
                    ]
                
                for idx, feature_title in enumerate(features):
                    PackageFeature.objects.create(
                        package=package,
                        title=feature_title,
                        included=True,
                        order=idx
                    )

        # پروژه‌ها و ویدیوها — Projects and video demos
        projects_data = [
            {
                'title': 'Angraweb Portfolio',
                'title_en': 'Angraweb Portfolio',
                'slug': 'angraweb-portfolio',
                'project_type': 'web',
                'description': 'Professional portfolio and company website.',
                'domain': 'angraweb.com',
                'url': 'https://angraweb.com',
                'technologies': 'Django, HTML, CSS, JavaScript',
                'featured': True,
                'order': 1,
            },
            {
                'title': 'Proje Örnekleri',
                'title_en': 'Project Samples',
                'slug': 'project-samples',
                'project_type': 'web',
                'description': 'Web and mobile project demos and samples.',
                'domain': '',
                'url': '',
                'technologies': 'Python, Django, React',
                'featured': True,
                'order': 2,
            },
        ]
        for p in projects_data:
            proj, created = Project.objects.get_or_create(slug=p['slug'], defaults=p)
            if created:
                try:
                    self.stdout.write(self.style.SUCCESS(f'Project created: {proj.title}'))
                except Exception:
                    pass

        # کپی ویدیوها به media و ایجاد ProjectVideo
        src_videos = Path(settings.BASE_DIR) / 'videos'
        media_root = Path(settings.MEDIA_ROOT)
        dest_videos = media_root / 'videos'
        if src_videos.exists():
            dest_videos.mkdir(parents=True, exist_ok=True)
            for mp4 in src_videos.glob('*.mp4'):
                dst = dest_videos / mp4.name
                if not dst.exists() or mp4.stat().st_mtime > dst.stat().st_mtime:
                    shutil.copy2(mp4, dst)
                rel = f'videos/{mp4.name}'
                pv, created = ProjectVideo.objects.get_or_create(
                    video_file=rel,
                    defaults={'title': mp4.stem, 'description': f'Demo: {mp4.stem}', 'order': 0, 'active': True}
                )
                if created:
                    try:
                        self.stdout.write(self.style.SUCCESS(f'ProjectVideo created: {pv.title}'))
                    except Exception:
                        pass

        self.stdout.write(self.style.SUCCESS('Initial data created successfully!'))
