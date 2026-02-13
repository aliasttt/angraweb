"""
Management command to add frequently asked questions
"""
import sys
from django.core.management.base import BaseCommand
from main.models import FAQ


class Command(BaseCommand):
    help = 'Add frequently asked questions'

    def handle(self, *args, **options):
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        faqs_data = [
            {
                'question': 'Web siteniz ne kadar sürede hazır olur?',
                'question_en': 'How long does it take to build a website?',
                'question_fa': 'وب‌سایت شما چقدر طول می‌کشد تا آماده شود؟',
                'question_ar': 'كم من الوقت يستغرق إعداد موقع الويب الخاص بك؟',
                'answer': 'Web sitenizin hazırlanma süresi projenin kapsamına ve karmaşıklığına bağlıdır. Basit bir kurumsal web sitesi genellikle 1-2 hafta içinde tamamlanır. E-ticaret siteleri ve özel platformlar ise 3-6 hafta sürebilir. Detaylı bir zaman çizelgesi için ücretsiz danışmanlık alabilirsiniz.',
                'answer_en': 'The time to build your website depends on the scope and complexity of the project. A simple corporate website is usually completed within 1-2 weeks. E-commerce sites and custom platforms can take 3-6 weeks. You can get a free consultation for a detailed timeline.',
                'answer_fa': 'زمان آماده شدن وب‌سایت شما به دامنه و پیچیدگی پروژه بستگی دارد. یک وب‌سایت شرکتی ساده معمولاً در 1-2 هفته تکمیل می‌شود. سایت‌های تجارت الکترونیک و پلتفرم‌های سفارشی می‌توانند 3-6 هفته طول بکشند. برای یک جدول زمانی دقیق می‌توانید مشاوره رایگان دریافت کنید.',
                'answer_ar': 'يعتمد الوقت اللازم لبناء موقع الويب الخاص بك على نطاق المشروع وتعقيده. عادة ما يتم إكمال موقع ويب شركة بسيط في غضون 1-2 أسبوع. يمكن أن تستغرق مواقع التجارة الإلكترونية والمنصات المخصصة 3-6 أسابيع. يمكنك الحصول على استشارة مجانية للحصول على جدول زمني مفصل.',
                'category': 'general',
                'order': 1,
                'active': True,
            },
            {
                'question': 'Web tasarım fiyatlarınız nedir?',
                'question_en': 'What are your web design prices?',
                'question_fa': 'قیمت‌های طراحی وب شما چقدر است؟',
                'question_ar': 'ما هي أسعار تصميم الويب الخاص بك؟',
                'answer': 'Fiyatlarımız projenin türüne ve özelliklerine göre değişmektedir. Temel paket 5,000 TL\'den başlar, profesyonel paketler 15,000 TL\'den başlar. E-ticaret siteleri ve özel platformlar için özel fiyatlandırma yapılmaktadır. Detaylı fiyat bilgisi için fiyat hesaplayıcımızı kullanabilir veya ücretsiz teklif alabilirsiniz.',
                'answer_en': 'Our prices vary depending on the type and features of the project. Basic package starts from 5,000 TL, professional packages start from 15,000 TL. Custom pricing is available for e-commerce sites and custom platforms. You can use our price calculator or get a free quote for detailed pricing information.',
                'answer_fa': 'قیمت‌های ما بسته به نوع و ویژگی‌های پروژه متفاوت است. پکیج پایه از 5,000 لیر شروع می‌شود، پکیج‌های حرفه‌ای از 15,000 لیر شروع می‌شوند. قیمت‌گذاری سفارشی برای سایت‌های تجارت الکترونیک و پلتفرم‌های سفارشی در دسترس است. می‌توانید از ماشین حساب قیمت ما استفاده کنید یا برای اطلاعات قیمت دقیق پیشنهاد رایگان دریافت کنید.',
                'answer_ar': 'تختلف أسعارنا حسب نوع المشروع وميزاته. تبدأ الحزمة الأساسية من 5,000 ليرة تركية، وتبدأ الحزم المهنية من 15,000 ليرة تركية. التسعير المخصص متاح لمواقع التجارة الإلكترونية والمنصات المخصصة. يمكنك استخدام حاسبة الأسعار الخاصة بنا أو الحصول على عرض أسعار مجاني للحصول على معلومات تسعير مفصلة.',
                'category': 'pricing',
                'order': 2,
                'active': True,
            },
            {
                'question': 'Web siteniz mobil uyumlu mu?',
                'question_en': 'Is your website mobile-friendly?',
                'question_fa': 'وب‌سایت شما با موبایل سازگار است؟',
                'question_ar': 'هل موقع الويب الخاص بك متوافق مع الهواتف المحمولة؟',
                'answer': 'Evet, tüm web sitelerimiz responsive (duyarlı) tasarıma sahiptir ve tüm cihazlarda (mobil telefon, tablet, masaüstü) mükemmel görünür ve çalışır. Mobil uyumluluk modern web tasarımının temel bir gereksinimidir ve tüm projelerimizde standart olarak dahildir.',
                'answer_en': 'Yes, all our websites have responsive design and look and work perfectly on all devices (mobile phone, tablet, desktop). Mobile compatibility is a fundamental requirement of modern web design and is included as standard in all our projects.',
                'answer_fa': 'بله، تمام وب‌سایت‌های ما طراحی ریسپانسیو دارند و در تمام دستگاه‌ها (تلفن همراه، تبلت، دسکتاپ) عالی به نظر می‌رسند و کار می‌کنند. سازگاری با موبایل یک نیاز اساسی طراحی وب مدرن است و به صورت استاندارد در تمام پروژه‌های ما گنجانده شده است.',
                'answer_ar': 'نعم، جميع مواقع الويب الخاصة بنا تتمتع بتصميم متجاوب وتبدو وتعمل بشكل مثالي على جميع الأجهزة (الهاتف المحمول والكمبيوتر اللوحي وسطح المكتب). التوافق مع الهاتف المحمول هو متطلب أساسي لتصميم الويب الحديث ومُدرج كمعيار في جميع مشاريعنا.',
                'category': 'technical',
                'order': 3,
                'active': True,
            },
            {
                'question': 'Web sitenizi kendim yönetebilir miyim?',
                'question_en': 'Can I manage my website myself?',
                'question_fa': 'آیا می‌توانم وب‌سایت خود را خودم مدیریت کنم؟',
                'question_ar': 'هل يمكنني إدارة موقع الويب الخاص بي بنفسي؟',
                'answer': 'Evet, tüm web sitelerimize kullanıcı dostu bir yönetim paneli (admin panel) dahildir. Bu panel sayesinde içerik ekleyebilir, düzenleyebilir, ürün yönetimi yapabilir ve site ayarlarınızı kolayca değiştirebilirsiniz. Ayrıca kapsamlı bir eğitim ve dokümantasyon sağlıyoruz.',
                'answer_en': 'Yes, all our websites include a user-friendly management panel (admin panel). Through this panel, you can add content, edit, manage products, and easily change your site settings. We also provide comprehensive training and documentation.',
                'answer_fa': 'بله، تمام وب‌سایت‌های ما شامل یک پنل مدیریت کاربرپسند (پنل ادمین) هستند. از طریق این پنل می‌توانید محتوا اضافه کنید، ویرایش کنید، محصولات را مدیریت کنید و تنظیمات سایت خود را به راحتی تغییر دهید. همچنین آموزش و مستندات جامع ارائه می‌دهیم.',
                'answer_ar': 'نعم، تتضمن جميع مواقع الويب الخاصة بنا لوحة إدارة سهلة الاستخدام (لوحة الإدارة). من خلال هذه اللوحة، يمكنك إضافة المحتوى وتحريره وإدارة المنتجات وتغيير إعدادات موقعك بسهولة. نوفر أيضًا تدريبًا ووثائق شاملة.',
                'category': 'services',
                'order': 4,
                'active': True,
            },
            {
                'question': 'SEO hizmeti dahil mi?',
                'question_en': 'Is SEO service included?',
                'question_fa': 'آیا خدمات SEO شامل است؟',
                'question_ar': 'هل تتضمن خدمة تحسين محركات البحث؟',
                'answer': 'Temel SEO optimizasyonu (meta etiketleri, başlık yapısı, hızlı yükleme) tüm paketlerimize dahildir. Ancak kapsamlı SEO hizmetleri (içerik optimizasyonu, backlink oluşturma, aylık raporlama) ayrı bir paket olarak sunulmaktadır. Detaylı bilgi için SEO sayfamızı ziyaret edebilirsiniz.',
                'answer_en': 'Basic SEO optimization (meta tags, title structure, fast loading) is included in all our packages. However, comprehensive SEO services (content optimization, backlink building, monthly reporting) are offered as a separate package. You can visit our SEO page for detailed information.',
                'answer_fa': 'بهینه‌سازی پایه SEO (متا تگ‌ها، ساختار عنوان، بارگذاری سریع) در تمام پکیج‌های ما گنجانده شده است. با این حال، خدمات جامع SEO (بهینه‌سازی محتوا، ساخت بک‌لینک، گزارش‌دهی ماهانه) به عنوان یک پکیج جداگانه ارائه می‌شود. برای اطلاعات دقیق می‌توانید صفحه SEO ما را بازدید کنید.',
                'answer_ar': 'يتم تضمين التحسين الأساسي لمحركات البحث (علامات التعريف وبنية العنوان والتحميل السريع) في جميع حزمنا. ومع ذلك، يتم تقديم خدمات تحسين محركات البحث الشاملة (تحسين المحتوى وبناء الروابط الخلفية والتقارير الشهرية) كحزمة منفصلة. يمكنك زيارة صفحة تحسين محركات البحث الخاصة بنا للحصول على معلومات مفصلة.',
                'category': 'services',
                'order': 5,
                'active': True,
            },
            {
                'question': 'Web siteniz hazır olduktan sonra destek sağlıyor musunuz?',
                'question_en': 'Do you provide support after the website is ready?',
                'question_fa': 'آیا پس از آماده شدن وب‌سایت پشتیبانی ارائه می‌دهید؟',
                'question_ar': 'هل تقدمون الدعم بعد جاهزية موقع الويب؟',
                'answer': 'Evet, tüm projelerimize teslimattan sonra 3 ay ücretsiz teknik destek sağlıyoruz. Bu süre içinde hata düzeltmeleri, küçük güncellemeler ve teknik sorunlar için destek veriyoruz. Ayrıca aylık bakım ve güncelleme paketleri de mevcuttur.',
                'answer_en': 'Yes, we provide 3 months of free technical support after delivery for all our projects. During this period, we provide support for bug fixes, minor updates, and technical issues. Monthly maintenance and update packages are also available.',
                'answer_fa': 'بله، برای تمام پروژه‌های ما 3 ماه پشتیبانی فنی رایگان پس از تحویل ارائه می‌دهیم. در این مدت، پشتیبانی برای رفع اشکال، به‌روزرسانی‌های جزئی و مسائل فنی ارائه می‌دهیم. همچنین پکیج‌های نگهداری و به‌روزرسانی ماهانه نیز در دسترس است.',
                'answer_ar': 'نعم، نوفر 3 أشهر من الدعم الفني المجاني بعد التسليم لجميع مشاريعنا. خلال هذه الفترة، نوفر الدعم لإصلاح الأخطاء والتحديثات الصغيرة والمشكلات الفنية. تتوفر أيضًا حزم الصيانة والتحديث الشهرية.',
                'category': 'support',
                'order': 6,
                'active': True,
            },
            {
                'question': 'Ödeme nasıl yapılır?',
                'question_en': 'How is payment made?',
                'question_fa': 'پرداخت چگونه انجام می‌شود؟',
                'question_ar': 'كيف يتم الدفع؟',
                'answer': 'Ödeme genellikle projenin başlangıcında %50 peşin ve teslimatta %50 olmak üzere iki taksitte yapılır. Büyük projeler için daha esnek ödeme planları sunuyoruz. Ödeme yöntemleri: banka havalesi, kredi kartı ve havale/EFT. Tüm ödemeler güvenli şekilde işlenir.',
                'answer_en': 'Payment is usually made in two installments: 50% advance at the start of the project and 50% upon delivery. We offer more flexible payment plans for large projects. Payment methods: bank transfer, credit card, and wire transfer/EFT. All payments are processed securely.',
                'answer_fa': 'پرداخت معمولاً در دو قسط انجام می‌شود: 50٪ پیش‌پرداخت در ابتدای پروژه و 50٪ در زمان تحویل. برای پروژه‌های بزرگ برنامه‌های پرداخت انعطاف‌پذیرتری ارائه می‌دهیم. روش‌های پرداخت: انتقال بانکی، کارت اعتباری و حواله/EFT. تمام پرداخت‌ها به صورت ایمن پردازش می‌شوند.',
                'answer_ar': 'عادة ما يتم الدفع على قسطين: 50٪ مقدم في بداية المشروع و 50٪ عند التسليم. نقدم خطط دفع أكثر مرونة للمشاريع الكبيرة. طرق الدفع: التحويل المصرفي وبطاقة الائتمان والحوالة/EFT. تتم معالجة جميع المدفوعات بشكل آمن.',
                'category': 'pricing',
                'order': 7,
                'active': True,
            },
            {
                'question': 'Hangi teknolojileri kullanıyorsunuz?',
                'question_en': 'What technologies do you use?',
                'question_fa': 'از چه فناوری‌هایی استفاده می‌کنید؟',
                'question_ar': 'ما هي التقنيات التي تستخدمونها؟',
                'answer': 'Modern ve güncel teknolojiler kullanıyoruz: Django (Python) backend için, HTML5, CSS3, JavaScript, Bootstrap frontend için. Veritabanı olarak PostgreSQL ve MySQL kullanıyoruz. Mobil uygulamalar için React Native ve Flutter kullanıyoruz. Detaylı teknoloji yığınımızı görmek için Technology Stack sayfamızı ziyaret edebilirsiniz.',
                'answer_en': 'We use modern and up-to-date technologies: Django (Python) for backend, HTML5, CSS3, JavaScript, Bootstrap for frontend. We use PostgreSQL and MySQL as databases. We use React Native and Flutter for mobile applications. You can visit our Technology Stack page to see our detailed technology stack.',
                'answer_fa': 'ما از فناوری‌های مدرن و به‌روز استفاده می‌کنیم: Django (Python) برای بک‌اند، HTML5، CSS3، JavaScript، Bootstrap برای فرانت‌اند. از PostgreSQL و MySQL به عنوان پایگاه داده استفاده می‌کنیم. برای برنامه‌های موبایل از React Native و Flutter استفاده می‌کنیم. می‌توانید صفحه Technology Stack ما را برای مشاهده پشته فناوری دقیق ما بازدید کنید.',
                'answer_ar': 'نستخدم تقنيات حديثة ومحدثة: Django (Python) للخلفية، HTML5 و CSS3 و JavaScript و Bootstrap للواجهة الأمامية. نستخدم PostgreSQL و MySQL كقواعد بيانات. نستخدم React Native و Flutter للتطبيقات المحمولة. يمكنك زيارة صفحة Technology Stack الخاصة بنا لرؤية مكدس التكنولوجيا المفصل لدينا.',
                'category': 'technical',
                'order': 8,
                'active': True,
            },
        ]

        created_count = 0
        for faq_data in faqs_data:
            # Check if FAQ already exists by question
            existing = FAQ.objects.filter(question=faq_data['question']).first()
            if not existing:
                FAQ.objects.create(**faq_data)
                created_count += 1
                print(f'[+] Created FAQ: {faq_data["question"][:50]}...')
            else:
                # Update existing FAQ
                for key, value in faq_data.items():
                    setattr(existing, key, value)
                existing.save()
                print(f'[~] Updated FAQ: {faq_data["question"][:50]}...')

        print(f'\n[OK] Completed! Created/Updated {created_count} FAQs!')
