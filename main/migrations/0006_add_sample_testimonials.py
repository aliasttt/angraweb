# Generated manually - sample testimonials

from django.db import migrations
from django.utils import timezone
from datetime import timedelta


def add_sample_testimonials(apps, schema_editor):
    Testimonial = apps.get_model('main', 'Testimonial')
    samples = [
        {
            'name': 'Ahmet Yılmaz',
            'company': 'Yılmaz Ticaret',
            'position': 'Yönetici',
            'content': 'Web sitemizi Angraweb ile yaptırdık. Çok profesyonel ve hızlı bir çalışma oldu. Müşteri memnuniyeti konusunda gerçekten hassaslar. Kesinlikle tavsiye ederim.',
            'content_en': 'We had our website made with Angraweb. Very professional and fast work. They are really sensitive about customer satisfaction. I definitely recommend.',
            'rating': 5,
            'featured': True,
            'order': 1,
            'active': True,
            'days_ago': 45,
        },
        {
            'name': 'Ayşe Demir',
            'company': 'Demir Gıda',
            'position': 'İşletme Sahibi',
            'content': 'E-ticaret sitemiz hayal ettiğimizden daha güzel oldu. Özellikle mobil uyumluluk ve hız konusunda çok başarılılar. Teşekkürler!',
            'content_en': 'Our e-commerce site turned out more beautiful than we imagined. They are very successful especially in mobile compatibility and speed. Thanks!',
            'rating': 5,
            'featured': True,
            'order': 2,
            'active': True,
            'days_ago': 30,
        },
        {
            'name': 'Mehmet Kaya',
            'company': '',
            'position': 'Serbest Çalışan',
            'content': 'Kurumsal web sitemi çok kısa sürede teslim ettiler. Fiyat-performans açısından piyasadaki en iyi seçenek. Destek ekibi de her zaman yanımızda.',
            'content_en': 'They delivered my corporate website in a very short time. The best option in the market in terms of price-performance. The support team is always with us.',
            'rating': 5,
            'featured': True,
            'order': 3,
            'active': True,
            'days_ago': 60,
        },
        {
            'name': 'Zeynep Öztürk',
            'company': 'Öztürk Danışmanlık',
            'position': 'Kurucu',
            'content': 'SEO ve tasarım konusunda uzman bir ekip. Sitemiz yayına girdikten sonra arama motoru sıralamalarımız belirgin şekilde yükseldi. Çok memnunuz.',
            'content_en': 'An expert team in SEO and design. After our site went live, our search engine rankings increased significantly. We are very satisfied.',
            'rating': 5,
            'featured': True,
            'order': 4,
            'active': True,
            'days_ago': 20,
        },
        {
            'name': 'Can Arslan',
            'company': 'Arslan Teknoloji',
            'position': 'IT Müdürü',
            'content': 'Teknik altyapı ve kod kalitesi çok iyi. Özelleştirme taleplerimizi hızlıca karşıladılar. Uzun vadeli çalışmak istediğimiz bir ekip.',
            'content_en': 'Technical infrastructure and code quality are very good. They quickly met our customization requests. A team we want to work with in the long term.',
            'rating': 5,
            'featured': False,
            'order': 5,
            'active': True,
            'days_ago': 15,
        },
        {
            'name': 'Elif Şahin',
            'company': 'Şahin Mimarlık',
            'position': 'Ortak',
            'content': 'Portfolyo sitemiz hem görsel hem işlevsel anlamda mükemmel oldu. İletişim ve teslim süreleri konusunda da çok titizler. Teşekkürler Angraweb!',
            'content_en': 'Our portfolio site was perfect both visually and functionally. They are also very meticulous about communication and delivery times. Thanks Angraweb!',
            'rating': 5,
            'featured': True,
            'order': 6,
            'active': True,
            'days_ago': 10,
        },
    ]
    for i, s in enumerate(samples):
        days_ago = s.pop('days_ago')
        obj = Testimonial.objects.create(**s)
        Testimonial.objects.filter(pk=obj.pk).update(
            created_at=timezone.now() - timedelta(days=days_ago)
        )


def remove_sample_testimonials(apps, schema_editor):
    Testimonial = apps.get_model('main', 'Testimonial')
    names = [
        'Ahmet Yılmaz', 'Ayşe Demir', 'Mehmet Kaya',
        'Zeynep Öztürk', 'Can Arslan', 'Elif Şahin'
    ]
    Testimonial.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_processstep_skill_timelineevent_casestudy'),
    ]

    operations = [
        migrations.RunPython(add_sample_testimonials, remove_sample_testimonials),
    ]
