"""
Management command to add new projects to the portfolio.
"""
import sys
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Project


class Command(BaseCommand):
    help = 'Add new projects to the portfolio'

    def handle(self, *args, **options):
        # Fix encoding for Windows console
        if sys.platform == 'win32':
            import codecs
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        projects_data = [
            {
                'title': 'Firmentshirt - Custom T-Shirt Printing',
                'title_en': 'Firmentshirt - Custom T-Shirt Printing',
                'title_fa': 'Firmentshirt - چاپ تی‌شرت سفارشی',
                'title_ar': 'Firmentshirt - طباعة القمصان المخصصة',
                'slug': 'firmentshirt-custom-tshirt-printing',
                'project_type': 'ecommerce',
                'description': 'E-commerce platform for custom printed T-shirts, caps, mugs, and aprons. Features include design studio, product customization, multi-language support (German/English), and integrated payment system.',
                'description_en': 'E-commerce platform for custom printed T-shirts, caps, mugs, and aprons. Features include design studio, product customization, multi-language support (German/English), and integrated payment system.',
                'description_fa': 'پلتفرم تجارت الکترونیک برای چاپ تی‌شرت، کلاه، فنجان و پیش‌بند سفارشی. شامل استودیو طراحی، سفارشی‌سازی محصول، پشتیبانی چندزبانه (آلمانی/انگلیسی) و سیستم پرداخت یکپارچه.',
                'description_ar': 'منصة التجارة الإلكترونية لطباعة القمصان والقمم والأكواب والمراييل المخصصة. تتضمن استوديو التصميم وتخصيص المنتجات ودعم متعدد اللغات (الألمانية/الإنجليزية) ونظام الدفع المتكامل.',
                'domain': 'firmentshirt.shop',
                'url': 'https://www.firmentshirt.shop/',
                'technologies': 'Django, Python, E-commerce, Payment Integration, Multi-language',
                'featured': True,
                'order': 3,
                'active': True,
            },
            {
                'title': 'Bonus Berlin - QR Menu & Loyalty Platform',
                'title_en': 'Bonus Berlin - QR Menu & Loyalty Platform',
                'title_fa': 'Bonus Berlin - پلتفرم منوی QR و وفاداری',
                'title_ar': 'Bonus Berlin - منصة قائمة QR والولاء',
                'slug': 'bonus-berlin-qr-menu-loyalty',
                'project_type': 'platform',
                'description': 'Complete QR menu and customer loyalty platform for restaurants and businesses. Features include digital menus, loyalty points system, customer reviews, push notifications, and business dashboard. Available as web app and mobile application.',
                'description_en': 'Complete QR menu and customer loyalty platform for restaurants and businesses. Features include digital menus, loyalty points system, customer reviews, push notifications, and business dashboard. Available as web app and mobile application.',
                'description_fa': 'پلتفرم کامل منوی QR و وفاداری مشتری برای رستوران‌ها و کسب‌وکارها. شامل منوهای دیجیتال، سیستم امتیاز وفاداری، نظرات مشتریان، اعلان‌های فوری و داشبورد کسب‌وکار. به صورت وب اپلیکیشن و اپلیکیشن موبایل در دسترس است.',
                'description_ar': 'منصة كاملة لقائمة QR وولاء العملاء للمطاعم والشركات. تتضمن القوائم الرقمية ونظام نقاط الولاء ومراجعات العملاء والإشعارات الفورية ولوحة تحكم الأعمال. متاح كتطبيق ويب وتطبيق جوال.',
                'domain': 'mybonusberlin.de',
                'url': 'https://mybonusberlin.de/',
                'technologies': 'Django, Python, React, Mobile App, Firebase, JWT Authentication',
                'featured': True,
                'order': 4,
                'active': True,
            },
            {
                'title': 'Kanoon Hamyari - Persian Community Services',
                'title_en': 'Kanoon Hamyari - Persian Community Services',
                'title_fa': 'کانون همیاری - خدمات جامع ایرانیان در ترکیه',
                'title_ar': 'كانون همياري - خدمات المجتمع الفارسي',
                'slug': 'kanoon-hamyari-persian-community',
                'project_type': 'platform',
                'description': 'Comprehensive community platform for Persian speakers in Turkey. Services include events, tours, real estate, advertising, educational consulting, legal affairs, and business support. Multi-language support (Persian, Turkish, English) with integrated social features.',
                'description_en': 'Comprehensive community platform for Persian speakers in Turkey. Services include events, tours, real estate, advertising, educational consulting, legal affairs, and business support. Multi-language support (Persian, Turkish, English) with integrated social features.',
                'description_fa': 'پلتفرم جامع جامعه برای فارسی‌زبانان در ترکیه. خدمات شامل رویدادها، تورها، املاک، تبلیغات، مشاوره تحصیلی، امور حقوقی و پشتیبانی کسب‌وکار. پشتیبانی چندزبانه (فارسی، ترکی، انگلیسی) با ویژگی‌های اجتماعی یکپارچه.',
                'description_ar': 'منصة مجتمع شاملة للناطقين بالفارسية في تركيا. الخدمات تشمل الأحداث والجولات والعقارات والإعلانات والاستشارات التعليمية والشؤون القانونية ودعم الأعمال. دعم متعدد اللغات (الفارسية والتركية والإنجليزية) مع ميزات اجتماعية متكاملة.',
                'domain': 'kanoonhamyari.com',
                'url': 'https://kanoonhamyari.com/',
                'technologies': 'Django, Python, Multi-language, Community Platform, Social Features',
                'featured': True,
                'order': 5,
                'active': True,
            },
            {
                'title': 'Gezgin Ustalar - Home Services Istanbul',
                'title_en': 'Gezgin Ustalar - Home Services Istanbul',
                'title_fa': 'Gezgin Ustalar - خدمات خانگی استانبول',
                'title_ar': 'Gezgin Ustalar - خدمات المنزل إسطنبول',
                'slug': 'gezgin-ustalar-home-services',
                'project_type': 'web',
                'description': 'Professional home services platform in Istanbul. Services include home decoration, repair & renovation, apartment painting, exterior insulation, flooring, elevator maintenance, and drilling services. Features service booking, portfolio gallery, and customer reviews.',
                'description_en': 'Professional home services platform in Istanbul. Services include home decoration, repair & renovation, apartment painting, exterior insulation, flooring, elevator maintenance, and drilling services. Features service booking, portfolio gallery, and customer reviews.',
                'description_fa': 'پلتفرم خدمات خانگی حرفه‌ای در استانبول. خدمات شامل دکوراسیون خانه، تعمیر و بازسازی، نقاشی آپارتمان، عایق‌بندی خارجی، کف‌پوش، نگهداری آسانسور و خدمات حفاری. شامل رزرو خدمات، گالری نمونه کارها و نظرات مشتریان.',
                'description_ar': 'منصة خدمات منزلية احترافية في إسطنبول. الخدمات تشمل ديكور المنزل والإصلاح والتجديد وطلاء الشقق والعزل الخارجي والأرضيات وصيانة المصاعد وخدمات الحفر. تتضمن حجز الخدمات ومعرض المحفظة ومراجعات العملاء.',
                'domain': 'gezginustalar.com',
                'url': 'https://gezginustalar.com/',
                'technologies': 'Django, Python, Service Booking, Portfolio Gallery, Reviews',
                'featured': True,
                'order': 6,
                'active': True,
            },
            {
                'title': 'Pier İnşaat - Construction & Sports Facilities',
                'title_en': 'Pier İnşaat - Construction & Sports Facilities',
                'title_fa': 'Pier İnşaat - ساخت‌وساز و تأسیسات ورزشی',
                'title_ar': 'Pier İnşaat - البناء والمرافق الرياضية',
                'slug': 'pier-insaat-construction',
                'project_type': 'web',
                'description': 'Construction company specializing in modern residential projects and sports facilities. Services include stadium construction, football field projects, infrastructure development, and premium residential complexes in Istanbul and Bursa. Features project portfolio, progress tracking, and client testimonials.',
                'description_en': 'Construction company specializing in modern residential projects and sports facilities. Services include stadium construction, football field projects, infrastructure development, and premium residential complexes in Istanbul and Bursa. Features project portfolio, progress tracking, and client testimonials.',
                'description_fa': 'شرکت ساخت‌وساز متخصص در پروژه‌های مسکونی مدرن و تأسیسات ورزشی. خدمات شامل ساخت استادیوم، پروژه‌های زمین فوتبال، توسعه زیرساخت و مجتمع‌های مسکونی پریمیوم در استانبول و بورسا. شامل نمونه کارها، ردیابی پیشرفت و نظرات مشتریان.',
                'description_ar': 'شركة بناء متخصصة في المشاريع السكنية الحديثة والمرافق الرياضية. الخدمات تشمل بناء الملاعب ومشاريع ملاعب كرة القدم وتطوير البنية التحتية والمجمعات السكنية المميزة في إسطنبول وبورصة. تتضمن محفظة المشاريع وتتبع التقدم وشهادات العملاء.',
                'domain': 'pierinsaat.com',
                'url': 'https://pierinsaat.com/',
                'technologies': 'Django, Python, Project Portfolio, Progress Tracking, Testimonials',
                'featured': True,
                'order': 7,
                'active': True,
            },
            {
                'title': 'Kalıcı Makyaj Monir - Permanent Makeup Studio',
                'title_en': 'Kalıcı Makyaj Monir - Permanent Makeup Studio',
                'title_fa': 'Kalıcı Makyaj Monir - استودیو آرایش دائمی',
                'title_ar': 'Kalıcı Makyaj Monir - استوديو المكياج الدائم',
                'slug': 'kalici-makyaj-monir-permanent-makeup',
                'project_type': 'web',
                'description': 'Premium beauty studio specializing in permanent makeup services in Istanbul. Services include microblading, eyebrow shading, permanent eyeliner, lip shading, tattoos, and piercings. Features service booking, portfolio gallery, customer reviews, and training programs.',
                'description_en': 'Premium beauty studio specializing in permanent makeup services in Istanbul. Services include microblading, eyebrow shading, permanent eyeliner, lip shading, tattoos, and piercings. Features service booking, portfolio gallery, customer reviews, and training programs.',
                'description_fa': 'استودیو زیبایی پریمیوم متخصص در خدمات آرایش دائمی در استانبول. خدمات شامل میکروبلیدینگ، سایه ابرو، خط چشم دائمی، سایه لب، خالکوبی و پیرسینگ. شامل رزرو خدمات، گالری نمونه کارها، نظرات مشتریان و برنامه‌های آموزشی.',
                'description_ar': 'استوديو جمال متميز متخصص في خدمات المكياج الدائم في إسطنبول. الخدمات تشمل الميكروبلادينغ وتظليل الحواجب وكحل العين الدائم وتظليل الشفاه والوشم والثقب. تتضمن حجز الخدمات ومعرض المحفظة ومراجعات العملاء وبرامج التدريب.',
                'domain': 'kalicimakyajmonir.com.tr',
                'url': 'https://kalicimakyajmonir.com.tr/',
                'technologies': 'Django, Python, Appointment Booking, Portfolio Gallery, Reviews',
                'featured': True,
                'order': 8,
                'active': True,
            },
            {
                'title': 'Hedef Sürücü Kursu - Driving School',
                'title_en': 'Hedef Sürücü Kursu - Driving School',
                'title_fa': 'Hedef Sürücü Kursu - آموزشگاه رانندگی',
                'title_ar': 'Hedef Sürücü Kursu - مدرسة القيادة',
                'slug': 'hedef-surucu-kursu-driving-school',
                'project_type': 'web',
                'description': 'Professional driving school website in Diyarbakır. Features include course information, instructor profiles, student testimonials, announcements, FAQ section, and contact forms. Modern design with high success rate display and international license information.',
                'description_en': 'Professional driving school website in Diyarbakır. Features include course information, instructor profiles, student testimonials, announcements, FAQ section, and contact forms. Modern design with high success rate display and international license information.',
                'description_fa': 'وب‌سایت آموزشگاه رانندگی حرفه‌ای در دیاربکر. شامل اطلاعات دوره، پروفایل مربیان، نظرات دانشجویان، اطلاعیه‌ها، بخش سوالات متداول و فرم‌های تماس. طراحی مدرن با نمایش نرخ موفقیت بالا و اطلاعات گواهینامه بین‌المللی.',
                'description_ar': 'موقع مدرسة القيادة الاحترافية في ديار بكر. يتضمن معلومات الدورة وملفات المدربين وشهادات الطلاب والإعلانات وقسم الأسئلة الشائعة ونماذج الاتصال. تصميم حديث مع عرض معدل النجاح العالي ومعلومات الترخيص الدولي.',
                'domain': 'hedefsürücükursları.com.tr',
                'url': 'https://xn--hedefsrckurslar-4vbbb82h.com.tr/',
                'technologies': 'Django, Python, Course Management, Testimonials, FAQ',
                'featured': True,
                'order': 9,
                'active': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for project_data in projects_data:
            slug = project_data.get('slug') or slugify(project_data['title'])
            project, created = Project.objects.get_or_create(
                slug=slug,
                defaults=project_data
            )
            
            if created:
                created_count += 1
                try:
                    self.stdout.write(self.style.SUCCESS(f'[+] Project created: {project.title}'))
                except UnicodeEncodeError:
                    self.stdout.write(self.style.SUCCESS(f'[+] Project created: {project.slug}'))
            else:
                # Update existing project
                for key, value in project_data.items():
                    if key != 'slug':  # Don't update slug
                        setattr(project, key, value)
                project.save()
                updated_count += 1
                try:
                    self.stdout.write(self.style.WARNING(f'[~] Project updated: {project.title}'))
                except UnicodeEncodeError:
                    self.stdout.write(self.style.WARNING(f'[~] Project updated: {project.slug}'))

        try:
            self.stdout.write(self.style.SUCCESS(
                f'\n[OK] Completed! Created: {created_count}, Updated: {updated_count}'
            ))
        except UnicodeEncodeError:
            self.stdout.write(self.style.SUCCESS(
                f'\n[OK] Completed! Created: {created_count}, Updated: {updated_count}'
            ))
