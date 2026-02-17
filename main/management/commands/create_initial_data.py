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
        
        # ایجاد پکیج‌ها با عنوان چندزبانه (TR, EN, FA, AR)
        PACKAGE_I18N = {
            'basic': {'title': 'Temel Paket', 'title_en': 'Basic Package', 'title_fa': 'پکیج پایه', 'title_ar': 'الباقة الأساسية'},
            'commercial': {'title': 'Ticari Paket', 'title_en': 'Commercial Package', 'title_fa': 'پکیج تجاری', 'title_ar': 'الباقة التجارية'},
            'professional': {'title': 'E-Ticaret Web Sitesi', 'title_en': 'E-commerce Website', 'title_fa': 'وبسایت فروشگاهی', 'title_ar': 'موقع التجارة الإلكترونية'},
            'custom': {'title': 'Özel Paket', 'title_en': 'Custom Package', 'title_fa': 'پکیج کاستوم', 'title_ar': 'الباقة المخصصة'},
        }
        FEATURE_I18N = {
            'طراحی ریسپانسیو': ('Responsive design', 'طراحی ریسپانسیو', 'التصميم المتجاوب'),
            'تا 5 صفحه': ('Up to 5 pages', 'تا ۵ صفحه', 'حتى 5 صفحات'),
            'فرم تماس': ('Contact form', 'فرم تماس', 'نموذج الاتصال'),
            'سئو پایه': ('Basic SEO', 'سئو پایه', 'تحسين أساسي'),
            'تا 10 صفحه': ('Up to 10 pages', 'تا ۱۰ صفحه', 'حتى 10 صفحات'),
            'پنل ادمین ساده': ('Simple admin panel', 'پنل ادمین ساده', 'لوحة إدارة بسيطة'),
            'دیتابیس پایه': ('Basic database', 'دیتابیس پایه', 'قاعدة بيانات أساسية'),
            'صفحات نامحدود': ('Unlimited pages', 'صفحات نامحدود', 'صفحات غير محدودة'),
            'پنل ادمین اختصاصی': ('Custom admin panel', 'پنل ادمین اختصاصی', 'لوحة إدارة مخصصة'),
            'دیتابیس پیشرفته': ('Advanced database', 'دیتابیس پیشرفته', 'قاعدة بيانات متقدمة'),
            'طراحی پلتفرم و شبکه اختصاصی': ('Custom platform design', 'طراحی پلتفرم و شبکه اختصاصی', 'تصميم منصة مخصصة'),
            'چندین وبسایت و پورتال هماهنگ': ('Multiple sites & portals', 'چندین وبسایت و پورتال', 'مواقع وب وبوابات'),
            'اپلیکیشن موبایل iOS و Android': ('iOS & Android app', 'اپلیکیشن موبایل', 'تطبيق iOS و Android'),
        }
        packages_data = [
            {'package_type': 'basic', 'price': 8000, 'currency': 'TL', 'order': 1, **PACKAGE_I18N['basic']},
            {'package_type': 'commercial', 'price': 15000, 'currency': 'TL', 'order': 2, 'popular': True, **PACKAGE_I18N['commercial']},
            {'package_type': 'professional', 'price': 35000, 'currency': 'TL', 'order': 3, **PACKAGE_I18N['professional']},
            {'package_type': 'custom', 'price': 0, 'custom_price_text': 'برای قیمت‌گذاری اختصاصی واتساپ پیام دهید', 'order': 4, **PACKAGE_I18N['custom']},
        ]
        for p in packages_data:
            pt = p['package_type']
            package, created = Package.objects.get_or_create(package_type=pt, defaults=p)
            package.title = p['title']
            package.title_en = p.get('title_en', '')
            package.title_fa = p.get('title_fa', '')
            package.title_ar = p.get('title_ar', '')
            package.save()
            if created:
                try:
                    self.stdout.write(self.style.SUCCESS(f'Package created: {package.title}'))
                except Exception:
                    pass
                if pt == 'basic':
                    feature_titles = ['طراحی ریسپانسیو', 'تا 5 صفحه', 'فرم تماس', 'سئو پایه']
                elif pt == 'commercial':
                    feature_titles = ['طراحی ریسپانسیو', 'تا 10 صفحه', 'پنل ادمین ساده', 'دیتابیس پایه']
                elif pt == 'professional':
                    feature_titles = ['طراحی ریسپانسیو', 'صفحات نامحدود', 'پنل ادمین اختصاصی', 'دیتابیس پیشرفته']
                else:
                    feature_titles = ['طراحی پلتفرم و شبکه اختصاصی', 'چندین وبسایت و پورتال هماهنگ', 'اپلیکیشن موبایل iOS و Android']
                for idx, ft in enumerate(feature_titles):
                    t = FEATURE_I18N.get(ft, (ft, ft, ft))
                    PackageFeature.objects.create(package=package, title=ft, title_en=t[0], title_fa=t[1], title_ar=t[2], included=True, order=idx)
            # به‌روزرسانی ویژگی‌های موجود
            for f in package.features.all():
                if not f.title_en and f.title in FEATURE_I18N:
                    t = FEATURE_I18N[f.title]
                    f.title_en, f.title_fa, f.title_ar = t[0], t[1], t[2]
                    f.save()

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
