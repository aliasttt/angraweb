"""
Management command to add default translations for services.
"""
import sys
from django.core.management.base import BaseCommand
from main.models import Service

# ترجمه‌های پیش‌فرض برای service ها
SERVICE_TRANSLATIONS = {
    'Uzman Web Tasarımı': {
        'title_fa': 'طراحی وب حرفه‌ای',
        'title_en': 'Professional Web Design',
        'title_ar': 'تصميم ويب احترافي',
        'description_fa': 'من وب‌سایت‌های مدرن و سریع برای رشد کسب‌وکار شما طراحی می‌کنم.',
        'description_en': 'I design modern and fast websites to grow your business.',
        'description_ar': 'أصمم مواقع ويب حديثة وسريعة لتنمية عملك.',
    },
    'E-Ticaret Çözümleri': {
        'title_fa': 'راه‌حل‌های تجارت الکترونیک',
        'title_en': 'E-Commerce Solutions',
        'title_ar': 'حلول التجارة الإلكترونية',
        'description_fa': 'فروشگاه اینترنتی حرفه‌ای برای افزایش فروش شما.',
        'description_en': 'Professional e-commerce site to increase your sales.',
        'description_ar': 'موقع تجارة إلكترونية احترافي لزيادة مبيعاتك.',
    },
    'Mobil Uyumlu Tasarım': {
        'title_fa': 'طراحی واکنش‌گرا',
        'title_en': 'Mobile Responsive Design',
        'title_ar': 'التصميم المتجاوب للجوال',
        'description_fa': 'وب‌سایت‌هایی که در تمام دستگاه‌ها عالی به نظر می‌رسند.',
        'description_en': 'Websites that look perfect on all devices.',
        'description_ar': 'مواقع ويب تبدو مثالية على جميع الأجهزة.',
    },
    'Hosting ve Yayınlama': {
        'title_fa': 'هاستینگ و انتشار',
        'title_en': 'Hosting and Publishing',
        'title_ar': 'الاستضافة والنشر',
        'description_fa': 'وب‌سایت شما را در سرورهای امن منتشر می‌کنم.',
        'description_en': 'I publish your website on secure servers.',
        'description_ar': 'أنشر موقعك على خوادم آمنة.',
    },
    'Kullanıcı Deneyimi Tasarımı': {
        'title_fa': 'طراحی تجربه کاربری',
        'title_en': 'User Experience Design',
        'title_ar': 'تصميم تجربة المستخدم',
        'description_fa': 'طراحی رابط‌های زیبا و کاربردی که مشتریان شما را تحت تأثیر قرار می‌دهد.',
        'description_en': 'Beautiful and functional interface designs that impress your customers.',
        'description_ar': 'تصاميم واجهات جميلة وعملية تثير إعجاب عملائك.',
    },
    'Hız ve SEO': {
        'title_fa': 'سرعت و سئو',
        'title_en': 'Speed and SEO',
        'title_ar': 'السرعة وتحسين محركات البحث',
        'description_fa': 'وب‌سایت شما را در Google به رتبه‌های بالا می‌رسانم.',
        'description_en': 'I bring your website to the top ranks in Google.',
        'description_ar': 'أجعل موقعك في المراتب العليا في Google.',
    },
}


class Command(BaseCommand):
    help = 'Add default translations for services'

    def handle(self, *args, **options):
        # Fix encoding for Windows console
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
        updated_count = 0
        
        self.stdout.write('Adding translations for Services...')
        
        for service in Service.objects.all():
            if service.title in SERVICE_TRANSLATIONS:
                translations = SERVICE_TRANSLATIONS[service.title]
                updated = False
                
                # Update title translations
                if not service.title_fa or service.title_fa == service.title:
                    service.title_fa = translations['title_fa']
                    updated = True
                if not service.title_en or service.title_en == service.title:
                    service.title_en = translations['title_en']
                    updated = True
                if not service.title_ar or service.title_ar == service.title:
                    service.title_ar = translations['title_ar']
                    updated = True
                
                # Update description translations
                if not service.description_fa or service.description_fa == service.description:
                    service.description_fa = translations['description_fa']
                    updated = True
                if not service.description_en or service.description_en == service.description:
                    service.description_en = translations['description_en']
                    updated = True
                if not service.description_ar or service.description_ar == service.description:
                    service.description_ar = translations['description_ar']
                    updated = True
                
                if updated:
                    service.save()
                    updated_count += 1
                    try:
                        self.stdout.write(f'  [OK] Updated: {service.title}')
                    except UnicodeEncodeError:
                        self.stdout.write(f'  [OK] Updated: Service ID {service.id}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Total services updated: {updated_count}'))
        self.stdout.write('\nService translations have been added successfully!')
