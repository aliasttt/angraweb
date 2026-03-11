# Data migration: improve website speed blog article content (TR) – clearer wording and structure

from django.db import migrations


def get_content_tr():
    return """<p class="blog-post-intro">Web sitesi hızı, günümüzde hem kullanıcı deneyimi hem de arama motoru sıralamaları için belirleyici bir unsurdur. Araştırmalara göre bir sayfa 3 saniyeden geç yüklenirse ziyaretçilerin büyük çoğunluğu siteyi terk eder. Bu nedenle hız optimizasyonu, dönüşüm oranlarını yükseltir ve Google sıralamalarını olumlu etkiler.</p>

<h2>Web Sitesi Neden Yavaş Olur?</h2>
<p>Yavaş açılan bir sitenin arkasında genellikle şu nedenler vardır:</p>
<ul>
<li>Optimize edilmemiş, ağır görseller</li>
<li>Yetersiz veya yavaş hosting altyapısı</li>
<li>Fazla sayıda JavaScript ve CSS dosyası</li>
<li>CDN kullanılmaması</li>
<li>Hatalı veya eksik sunucu yapılandırması</li>
</ul>
<p>Bu faktörler bir araya geldiğinde performans ciddi biçimde düşer.</p>

<h2>Web Sitesi Hızını Artıran Teknikler</h2>
<p>Aşağıdaki adımlar, site hızınızı belirgin şekilde iyileştirmenize yardımcı olur.</p>

<h3>Görsel Optimizasyonu</h3>
<p>Görseller çoğu sitede en fazla yer kaplayan öğedir. Bunları hafifletmek için:</p>
<ul>
<li>Mümkün olduğunda WebP formatını kullanın</li>
<li>Görselleri sıkıştırın (kayıpsız veya hafif kayıplı)</li>
<li>Lazy loading ile sayfa açılışını hızlandırın</li>
</ul>

<h3>CDN Kullanımı</h3>
<p>Content Delivery Network (CDN), içeriğinizi dünya genelindeki sunuculara dağıtır. Ziyaretçiler en yakın noktadan veri çeker; böylece sayfa daha hızlı açılır.</p>

<h3>Hosting Altyapısını İyileştirmek</h3>
<p>Hosting seçimi, site hızını doğrudan etkiler. Özellikle büyük veya trafiği yüksek projelerde VPS veya cloud hosting tercih edin.</p>
<p class="blog-post-cta">👉 <a href="/tr/hosting/">VPS Hosting Services</a> sayfamızdan hosting seçeneklerini inceleyebilirsiniz.</p>

<h3>Kod Optimizasyonu</h3>
<p>Gereksiz CSS ve JavaScript dosyaları hem boyutu hem de istek sayısını artırır. Bunları azaltmak için:</p>
<ul>
<li>Minify (sıkıştırma) uygulayın</li>
<li>Script birleştirme (bundling) yapın</li>
<li>Kullanılmayan eklentileri kaldırın</li>
</ul>

<h2>Web Sitesi Hızı SEO'yu Nasıl Etkiler?</h2>
<p>Google, sayfa hızını resmi bir sıralama faktörü olarak kullanır. Hızlı siteler:</p>
<ul>
<li>Daha iyi kullanıcı deneyimi sunar</li>
<li>Bounce rate’i düşürür</li>
<li>Arama sonuçlarında daha üst sıralarda yer alır</li>
</ul>
<p class="blog-post-cta">👉 SEO hizmetleri için <a href="/tr/seo/">SEO Consulting Services</a> sayfamızı inceleyebilirsiniz.</p>

<h2>Sonuç</h2>
<p>Web sitesi hızını artırmak yalnızca teknik bir iyileştirme değil; dijital başarı için kritik bir yatırımdır. Doğru hosting, optimize görseller ve temiz kod yapısıyla sitenizin performansını önemli ölçüde yükseltebilirsiniz.</p>

<h2 class="blog-post-faq-title">Sıkça Sorulan Sorular</h2>
<div class="blog-post-faq">
<p><strong>Web sitesi hızı kaç saniye olmalı?</strong><br>İdeal açılış süresi 2–3 saniye aralığındadır.</p>
<p><strong>Web sitesi hızını nasıl test ederim?</strong><br>Google PageSpeed Insights veya GTmetrix gibi araçlarla ücretsiz test yapabilirsiniz.</p>
<p><strong>Hosting site hızını etkiler mi?</strong><br>Evet. Hosting altyapısı, sitenizin performansını doğrudan etkiler.</p>
</div>"""


def update_post(apps, schema_editor):
    BlogPost = apps.get_model('main', 'BlogPost')
    post = BlogPost.objects.filter(slug='web-sitesi-hizi-nasil-artirilir').first()
    if not post:
        return
    post.content = get_content_tr()
    post.save(update_fields=['content'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_update_blog_website_speed_article'),
    ]

    operations = [
        migrations.RunPython(update_post, noop),
    ]
