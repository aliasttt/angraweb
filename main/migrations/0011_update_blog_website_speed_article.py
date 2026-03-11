# Data migration: update website speed blog article content to latest copy

from django.db import migrations


def get_content_tr():
    return """<p>Web sitesi hızı, modern internet dünyasında hem kullanıcı deneyimi hem de SEO performansı açısından kritik bir faktördür. Google'a göre bir web sitesi 3 saniyeden uzun sürede açılıyorsa kullanıcıların büyük bir kısmı siteyi terk eder.</p>
<p>Bu nedenle web sitesi hızını optimize etmek, hem dönüşüm oranlarını artırır hem de Google sıralamalarını olumlu etkiler.</p>

<h2>Web Sitesi Neden Yavaş Olur?</h2>
<p>Bir web sitesinin yavaş olmasının birçok nedeni olabilir:</p>
<ul>
<li>Büyük ve optimize edilmemiş görseller</li>
<li>Yavaş hosting altyapısı</li>
<li>Fazla JavaScript ve CSS dosyası</li>
<li>CDN kullanılmaması</li>
<li>Sunucu yapılandırma hataları</li>
</ul>
<p>Bu faktörler birleştiğinde web sitesi performansı ciddi şekilde düşebilir.</p>

<h2>Web Sitesi Hızını Artıran Teknikler</h2>
<p>Web sitesi performansını artırmak için aşağıdaki teknikler kullanılabilir.</p>

<h3>Görsel Optimizasyonu</h3>
<p>Web sitelerindeki görseller genellikle en büyük dosya boyutuna sahiptir. Görselleri optimize etmek için:</p>
<ul>
<li>WebP formatı kullanın</li>
<li>Görselleri sıkıştırın</li>
<li>Lazy loading kullanın</li>
</ul>

<h3>CDN Kullanımı</h3>
<p>Content Delivery Network (CDN), web sitenizin içeriğini dünya çapında farklı sunuculara dağıtır. Bu sayede kullanıcılar en yakın sunucudan içerik alır ve site daha hızlı açılır.</p>

<h3>Hosting Altyapısını İyileştirmek</h3>
<p>Hosting seçimi site hızını doğrudan etkiler. Özellikle büyük projelerde VPS veya cloud hosting tercih edilmelidir.</p>
<p>👉 Hosting seçeneklerini incelemek için <a href="/tr/hosting/">VPS Hosting Services</a> sayfamıza göz atabilirsiniz.</p>

<h3>Kod Optimizasyonu</h3>
<p>Web sitelerinde gereksiz CSS ve JavaScript dosyaları performansı düşürebilir.</p>
<p>Bunları azaltmak için:</p>
<ul>
<li>Minify işlemi</li>
<li>Script birleştirme</li>
<li>Gereksiz plugin kaldırma</li>
</ul>
<p>gibi teknikler uygulanabilir.</p>

<h2>Web Sitesi Hızı SEO'yu Nasıl Etkiler?</h2>
<p>Google, site hızını resmi bir sıralama faktörü olarak kullanmaktadır. Hızlı web siteleri:</p>
<ul>
<li>Daha iyi kullanıcı deneyimi sunar</li>
<li>Daha düşük bounce rate sağlar</li>
<li>Daha yüksek SEO sıralaması elde eder</li>
</ul>
<p>SEO hakkında daha fazla bilgi için<br>👉 <a href="/tr/seo/">SEO Consulting Services</a> sayfamızı inceleyebilirsiniz.</p>

<h2>Sonuç</h2>
<p>Web sitesi hızını artırmak, yalnızca teknik bir optimizasyon değil aynı zamanda dijital başarı için kritik bir yatırımdır. Doğru hosting, optimize edilmiş görseller ve temiz kod yapısı sayesinde web sitenizin performansını önemli ölçüde artırabilirsiniz.</p>

<h2>SSS</h2>
<p><strong>Web sitesi hızı kaç saniye olmalı?</strong><br>İdeal web sitesi açılış süresi 2–3 saniye arasındadır.</p>
<p><strong>Web sitesi hızını nasıl test ederim?</strong><br>Google PageSpeed Insights veya GTmetrix gibi araçlarla test edebilirsiniz.</p>
<p><strong>Hosting site hızını etkiler mi?</strong><br>Evet. Hosting altyapısı web sitesi performansını doğrudan etkiler.</p>"""


def get_content_en():
    return """<p>Website speed plays a crucial role in modern digital experiences. According to Google, if a website takes longer than 3 seconds to load, most users will leave the page.</p>
<p>Optimizing website speed improves both SEO performance and conversion rates.</p>

<h2>Why Websites Become Slow</h2>
<p>Several factors can cause slow website performance:</p>
<ul>
<li>Large unoptimized images</li>
<li>Poor hosting infrastructure</li>
<li>Excessive JavaScript and CSS files</li>
<li>Lack of CDN usage</li>
<li>Server configuration issues</li>
</ul>

<h2>Techniques to Improve Website Speed</h2>

<h3>Image Optimization</h3>
<p>Images often represent the largest portion of website data.</p>
<p>To optimize images:</p>
<ul>
<li>Use WebP format</li>
<li>Compress images</li>
<li>Enable lazy loading</li>
</ul>

<h3>Use a CDN</h3>
<p>A Content Delivery Network distributes your website content across global servers.</p>
<p>This allows users to load your site from the closest location.</p>

<h3>Improve Hosting Infrastructure</h3>
<p>Choosing the right hosting provider is critical.</p>
<p>For scalable websites, VPS or cloud hosting is recommended.</p>
<p>👉 Learn more about hosting on our <a href="/en/hosting/">VPS Hosting Services</a> page.</p>

<h3>Code Optimization</h3>
<p>Reduce unnecessary JavaScript and CSS files by:</p>
<ul>
<li>Minification</li>
<li>Script bundling</li>
<li>Removing unused plugins</li>
</ul>

<h2>How Website Speed Affects SEO</h2>
<p>Google officially considers page speed as a ranking factor.</p>
<p>Fast websites provide:</p>
<ul>
<li>Better user experience</li>
<li>Lower bounce rate</li>
<li>Higher search rankings</li>
</ul>
<p>For more SEO insights visit<br>👉 <a href="/en/seo/">SEO Consulting Services</a></p>

<h2>Conclusion</h2>
<p>Website speed optimization is not just a technical improvement but a key investment in digital success.</p>
<p>With optimized images, fast hosting, and clean code structure, your website can achieve significantly better performance.</p>

<h2>FAQ</h2>
<p><strong>How long should a website take to load?</strong><br>Ideal load time is 2–3 seconds.</p>
<p><strong>How can I test website speed?</strong><br>Use tools like Google PageSpeed Insights or GTmetrix.</p>
<p><strong>Does hosting affect site speed?</strong><br>Yes. Hosting infrastructure directly affects website performance.</p>"""


def update_post(apps, schema_editor):
    BlogPost = apps.get_model('main', 'BlogPost')
    post = BlogPost.objects.filter(slug='web-sitesi-hizi-nasil-artirilir').first()
    if not post:
        return
    post.title = 'Web Sitesi Açılış Hızı Nasıl Artırılır? (SEO ve Performans Rehberi)'
    post.title_en = 'How to Improve Website Speed (SEO & Performance Guide)'
    post.excerpt = 'Web sitesi hızını artırmak SEO, kullanıcı deneyimi ve dönüşüm oranları için kritik öneme sahiptir. Bu rehberde site hızını artıran teknikleri öğrenin.'
    post.excerpt_en = 'Website speed is critical for SEO, user experience, and conversions. Learn the best techniques to improve website loading speed in this guide.'
    post.content = get_content_tr()
    post.content_en = get_content_en()
    post.save(update_fields=['title', 'title_en', 'excerpt', 'excerpt_en', 'content', 'content_en'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_add_blog_website_speed_article'),
    ]

    operations = [
        migrations.RunPython(update_post, noop),
    ]
