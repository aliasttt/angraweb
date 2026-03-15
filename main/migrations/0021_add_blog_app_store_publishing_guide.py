# Data migration: add blog article "App Store'a Uygulama Yayınlama Rehberi / How to Publish an App on the App Store"

from django.db import migrations
from django.utils import timezone


def build_content_tr():
    return """<section class="blog-intro">
<p>Bir mobil uygulama geliştirdikten sonra en önemli adımlardan biri uygulamayı App Store'da yayınlamaktır. Ancak birçok geliştirici ve startup bu süreçte teknik gereksinimler, politika kuralları ve inceleme süreci nedeniyle zorluklarla karşılaşabilir.</p>
<p><strong>App Store uygulama yayınlama</strong> süreci belirli kurallara ve hazırlık adımlarına bağlıdır. Uygulama yalnızca geliştirilmekle kalmaz; Apple politikalarına uygun şekilde hazırlanmalı, <strong>Apple Developer hesabı</strong> ile doğru kanallar kullanılmalı ve <strong>App Store uygulama yükleme</strong> adımları eksiksiz tamamlanmalıdır.</p>
<p>Bu rehberde <strong>iOS uygulama yayınlama</strong> sürecini adım adım inceliyoruz: Apple Developer Program kaydından App Store Connect kullanımına, Xcode ile yüklemeye ve inceleme sürecine kadar. <strong>iOS uygulama geliştirme</strong> tamamlandıktan sonra mağazada görünür olmak için izlemeniz gereken yolu netleştireceğiz.</p>
</section>

<h2>Apple Developer Hesabı Oluşturma</h2>
<p>App Store'da uygulama yayınlayabilmek için öncelikle bir <strong>Apple Developer</strong> hesabı oluşturmanız gerekir. Bu hesap olmadan <strong>App Store uygulama yükleme</strong> yapılamaz.</p>

<h3>Gereksinimler</h3>
<ul>
<li>Geçerli bir Apple ID (Apple kimliği)</li>
<li>Apple Developer Program'a yıllık üyelik ücreti (99 USD)</li>
<li>Hesap doğrulama ve sözleşmelerin onaylanması</li>
</ul>
<p>Apple Developer Program yıllık 99 dolar ücretlidir. Bu hesap ile uygulama yükleyebilir, test araçlarına erişebilir ve App Store Connect üzerinden uygulamanızı yönetebilirsiniz.</p>

<h2>Uygulama Hazırlığı</h2>
<p>Uygulama yayınlanmadan önce teknik ve içerik gereksinimlerinin tamamlanmış olması gerekir. Eksik veya hatalı hazırlık inceleme sürecinde red veya gecikmeye neden olur.</p>

<h3>Teknik Gereksinimler</h3>
<ul>
<li>Uygulama stabil çalışmalı; crash ve kritik hatalar giderilmiş olmalı</li>
<li>App Store İnsan Arayüzü ve İçerik Kurallarına uyum</li>
<li>Kullanıcı gizliliği politikası (URL veya uygulama içi erişilebilir)</li>
<li>Gerekli izinler (konum, kamera vb.) doğru ve açıklayıcı kullanılmalı</li>
</ul>

<h3>Mağaza Sayfası İçeriği</h3>
<ul>
<li>Uygulama adı ve alt başlık</li>
<li>Uygulama açıklaması (Türkçe ve/veya hedef diller)</li>
<li>Ekran görüntüleri (farklı cihaz boyutları için)</li>
<li>Uygulama ikonu (1024x1024 px)</li>
<li>Anahtar kelimeler (ASO için)</li>
<li>Kategori ve yaş derecelendirmesi</li>
</ul>
<p>Profesyonel görsel ve metin hazırlığı için <a href="/tr/web-tasarim/profesyonel-web-tasarim/">profesyonel web tasarım</a> ve ürün tasarımı hizmetlerimiz, uygulama mağaza sayfası ve marka tutarlılığı konusunda size yardımcı olabilir.</p>

<h2>App Store Connect Kullanımı</h2>
<p>Apple, uygulama yönetimi ve <strong>App Store uygulama yayınlama</strong> süreci için App Store Connect platformunu kullanır.</p>

<h3>App Store Connect ile Yapılanlar</h3>
<ul>
<li>Yeni uygulama kaydı oluşturma</li>
<li>Uygulama adı, bundle ID, kategori ve açıklama girişi</li>
<li>Versiyon ve build yönetimi</li>
<li>İstatistik, satış ve indirme takibi</li>
<li>TestFlight ile beta dağıtımı</li>
</ul>
<p>Yeni bir uygulama eklerken uygulama adı, bundle ID (Xcode ile aynı olmalı), kategori, açıklama ve anahtar kelimeler girilir. Bu bilgiler App Store'da uygulamanızın nasıl görüneceğini belirler.</p>

<h2>Xcode ile Uygulama Yükleme</h2>
<p><strong>App Store uygulama yükleme</strong> işlemi genellikle Xcode üzerinden yapılır. macOS ve Xcode kurulu bir geliştirme ortamı gerekir.</p>

<h3>Adımlar</h3>
<ul>
<li><strong>1.</strong> Xcode'da projeyi açın ve hedef cihazı "Any iOS Device (arm64)" olarak seçin.</li>
<li><strong>2.</strong> Product → Archive ile arşiv oluşturun.</li>
<li><strong>3.</strong> Organizer penceresinde "Distribute App" seçin; "App Store Connect" seçeneğini işaretleyin.</li>
<li><strong>4.</strong> Yükleme tamamlandığında build, App Store Connect'te "TestFlight ve App Store Gönderimi" altında görünür; bu build'i yeni bir sürümle ilişkilendirip incelemeye gönderin.</li>
</ul>
<p>Bu işlem tamamlandığında uygulama Apple inceleme kuyruğuna girer. <strong>iOS uygulama geliştirme</strong> ve yayınlama sürecinde teknik destek için <a href="/tr/mobile-app/">mobil uygulama geliştirme</a> hizmet sayfamızı inceleyebilirsiniz.</p>

<h2>App Store İnceleme Süreci</h2>
<p>Apple, uygulamaları yayınlamadan önce inceleme sürecinden geçirir. Bu süreç <strong>App Store uygulama yayınlama</strong> için zorunludur.</p>

<h3>Değerlendirilen Kriterler</h3>
<ul>
<li>Uygulama kararlı mı, crash veya belirgin hata var mı?</li>
<li>Kullanıcı deneyimi ve arayüz kurallara uygun mu?</li>
<li>Gizlilik politikası ve veri kullanımı açık mı?</li>
<li>Spam, yanıltıcı içerik veya politika ihlali var mı?</li>
</ul>
<p>İnceleme süreci genellikle 1–3 iş günü sürer. Uygulama kurallara uygun değilse Apple düzeltme talep eder veya reddeder; e-posta ile gerekçe bildirilir.</p>

<h2>Tasarım ve Kullanıcı Deneyimi Beklentileri</h2>
<p>Apple, uygulama tasarımı ve kullanıcı deneyimi konusunda yüksek standartlar bekler. Güncel tasarım trendleri hem inceleme sürecinde olumlu izlenim bırakır hem de kullanıcıların uygulamanızı tercih etmesine yardımcı olur.</p>

<h3>Öne Çıkan Unsurlar</h3>
<ul>
<li><strong>Dark mode desteği:</strong> iOS'ta sistem temasına uyum (açık/koyu) birçok uygulama için beklenen bir özelliktir.</li>
<li><strong>Net arayüz ve tipografi:</strong> Okunabilir metin, tutarlı spacing ve erişilebilirlik (VoiceOver uyumu) önemlidir.</li>
<li><strong>Hafif animasyon ve 3D öğeler:</strong> Abartılmadan kullanıldığında modern ve kaliteli bir his verir.</li>
<li><strong>Modüler layout (Bento tarzı kartlar):</strong> İçeriğin düzenli sunulduğu arayüzler kullanıcı deneyimini güçlendirir.</li>
<li><strong>Yapay zeka ve kişiselleştirme:</strong> Öneri veya akıllı özellikler, kullanıcı değeri sunuyorsa artı olarak değerlendirilir.</li>
</ul>
<p>Bu unsurlar <strong>iOS uygulama yayınlama</strong> sonrası kullanıcı memnuniyeti ve mağaza puanları için de faydalıdır.</p>

<h2>Uygulama Yayınlandıktan Sonra</h2>
<p>Uygulama yayınlandıktan sonra süreç bitmez. Asıl hedef kullanıcıları uygulamaya çekmek ve elde tutmaktır.</p>

<h3>Yayın Sonrası Yapılabilecekler</h3>
<ul>
<li><strong>App Store Optimization (ASO):</strong> Anahtar kelimeler, açıklama ve ekran görüntülerini veriye göre iyileştirmek</li>
<li>Kullanıcı yorumlarını takip etmek ve yanıtlamak</li>
<li>Düzenli güncellemeler ve yeni özellikler yayınlamak</li>
<li>Pazarlama ve tanıtım kampanyaları (web sitesi, sosyal medya, reklam)</li>
</ul>
<p>Bu çalışmalar uygulamanın daha fazla indirme ve aktif kullanıcıya ulaşmasını sağlar.</p>

<h2>Sonuç ve Sonraki Adımlar</h2>
<p><strong>App Store'a uygulama yayınlama</strong> doğru planlama, teknik hazırlık ve politika uyumu gerektirir. <strong>Apple Developer hesabı</strong> oluşturmak, uygulamayı kurallara uygun hazırlamak, App Store Connect üzerinden bilgileri girmek ve Xcode ile build yükleyip incelemeye göndermek sürecin temel adımlarıdır. Kurallara uygun ve kaliteli bir <strong>iOS uygulama geliştirme</strong> süreci, incelemeyi kolaylaştırır ve uygulamanın mağazada başarılı olma ihtimalini artırır.</p>
<p><strong>Hemen harekete geçin:</strong> iOS uygulamanızı geliştirme veya yayınlama sürecinde destek almak için <a href="/tr/contact/">iletişim</a> sayfamızdan bize ulaşabilir veya <a href="/tr/mobile-app/">mobil uygulama geliştirme</a> hizmetlerimizi inceleyebilirsiniz.</p>

<h2>Sıkça Sorulan Sorular</h2>

<h3>App Store'a uygulama yüklemek ücretli mi?</h3>
<p>Evet. App Store'da uygulama yayınlamak için Apple Developer Program üyeliği gerekir; bu üyelik yıllık 99 USD ücretlidir. Üyelik olmadan <strong>App Store uygulama yükleme</strong> yapılamaz.</p>

<h3>App Store inceleme süreci ne kadar sürer?</h3>
<p>Genellikle 1–3 iş günü sürer. Yoğunluk dönemlerinde veya eksik bilgi/uyumsuzluk durumunda süre uzayabilir. İnceleme sonucu e-posta ile bildirilir.</p>

<h3>Her uygulama App Store'da yayınlanabilir mi?</h3>
<p>Hayır. Apple'ın İnsan Arayüzü Kuralları, Gizlilik ve İçerik Kurallarına uymayan uygulamalar reddedilebilir. Politikaları önceden okuyup uygulamanızı buna göre hazırlamanız önerilir.</p>

<h3>TestFlight ile beta testi zorunlu mu?</h3>
<p>Zorunlu değildir ancak önerilir. TestFlight ile gerçek cihazlarda test yaparak hataları inceleme öncesi tespit edebilir ve kullanıcı deneyimini iyileştirebilirsiniz.</p>"""


def build_content_en():
    return """<section class="blog-intro">
<p>After developing a mobile application, one of the most important steps is publishing it on the Apple App Store. Many developers and startups, however, face challenges due to technical requirements, policy rules and the review process.</p>
<p>The <strong>App Store</strong> publishing process depends on specific rules and preparation steps. The app must not only be built; it must be prepared in line with Apple's policies, and you need an <strong>Apple Developer account</strong> and the correct <strong>App Store submission</strong> steps.</p>
<p>In this guide we walk through <strong>iOS app publishing</strong> step by step: from Apple Developer Program registration to using App Store Connect, uploading with Xcode and the review process. We clarify the path you need to follow so your app is visible in the store after <strong>iOS app development</strong> is complete.</p>
</section>

<h2>Create an Apple Developer Account</h2>
<p>To publish apps on the App Store you must first create an <strong>Apple Developer</strong> account. Without it, you cannot upload apps to the App Store.</p>

<h3>Requirements</h3>
<ul>
<li>A valid Apple ID</li>
<li>Apple Developer Program yearly fee (99 USD)</li>
<li>Account verification and agreement acceptance</li>
</ul>
<p>The Apple Developer Program costs 99 USD per year. With this account you can upload apps, use test tools and manage your app via App Store Connect.</p>

<h2>Application Preparation</h2>
<p>Before release, technical and content requirements must be complete. Missing or incorrect preparation can lead to rejection or delay during review.</p>

<h3>Technical Requirements</h3>
<ul>
<li>Stable app; crashes and critical bugs fixed</li>
<li>Compliance with App Store Human Interface and content guidelines</li>
<li>Privacy policy (URL or in-app access)</li>
<li>Required permissions (location, camera, etc.) used correctly and with clear explanations</li>
</ul>

<h3>Store Listing Content</h3>
<ul>
<li>App name and subtitle</li>
<li>App description (and/or target languages)</li>
<li>Screenshots (for required device sizes)</li>
<li>App icon (1024x1024 px)</li>
<li>Keywords (for ASO)</li>
<li>Category and age rating</li>
</ul>
<p>For professional visuals and copy, our <a href="/en/web-design/professional-web-design/">professional web design</a> and product design services can help with your store page and brand consistency.</p>

<h2>Using App Store Connect</h2>
<p>Apple uses App Store Connect for app management and the <strong>publish app on App Store</strong> workflow.</p>

<h3>What You Do in App Store Connect</h3>
<ul>
<li>Create a new app record</li>
<li>Enter app name, bundle ID, category and description</li>
<li>Manage versions and builds</li>
<li>Track analytics, sales and downloads</li>
<li>Distribute beta via TestFlight</li>
</ul>
<p>When adding a new app you enter app name, bundle ID (must match Xcode), category, description and keywords. This information defines how your app appears on the App Store.</p>

<h2>Uploading with Xcode</h2>
<p><strong>App Store submission</strong> is typically done through Xcode. You need a Mac and Xcode installed.</p>

<h3>Steps</h3>
<ul>
<li><strong>1.</strong> Open the project in Xcode and set the destination to "Any iOS Device (arm64)".</li>
<li><strong>2.</strong> Create an archive via Product → Archive.</li>
<li><strong>3.</strong> In the Organizer window choose "Distribute App" and select "App Store Connect".</li>
<li><strong>4.</strong> After upload, the build appears in App Store Connect under "TestFlight and App Store"; attach it to a new version and submit for review.</li>
</ul>
<p>Once this is done, the app enters Apple's review queue. For technical support during <strong>iOS app development</strong> and publishing, see our <a href="/en/mobile-app/">mobile app development</a> services page.</p>

<h2>App Review Process</h2>
<p>Apple reviews every app before release. This step is required to <strong>publish app on App Store</strong>.</p>

<h3>What Apple Evaluates</h3>
<ul>
<li>Is the app stable; any crashes or obvious bugs?</li>
<li>Does the UX and interface comply with guidelines?</li>
<li>Are privacy policy and data usage clear?</li>
<li>Any spam, misleading content or policy violations?</li>
</ul>
<p>Review usually takes 1–3 business days. If the app does not comply, Apple may request changes or reject it and explain by email.</p>

<h2>Design and User Experience Expectations</h2>
<p>Apple expects high standards for app design and user experience. Current design trends both leave a positive impression during review and help users choose your app.</p>

<h3>Notable Elements</h3>
<ul>
<li><strong>Dark mode:</strong> Adapting to system light/dark theme is expected for many apps.</li>
<li><strong>Clear UI and typography:</strong> Readable text, consistent spacing and accessibility (e.g. VoiceOver) matter.</li>
<li><strong>Subtle animation and 3D:</strong> Used in balance, they convey a modern, quality feel.</li>
<li><strong>Modular layout (Bento-style cards):</strong> Organized content layout improves UX.</li>
<li><strong>AI and personalization:</strong> Recommendations or smart features add value when they serve the user.</li>
</ul>
<p>These elements also support user satisfaction and store ratings after <strong>iOS app publishing</strong>.</p>

<h2>After Publishing</h2>
<p>Publishing is not the end. The real goal is to attract and retain users.</p>

<h3>Post-Launch Activities</h3>
<ul>
<li><strong>App Store Optimization (ASO):</strong> Improve keywords, description and screenshots based on data</li>
<li>Monitor and respond to user reviews</li>
<li>Release regular updates and new features</li>
<li>Marketing (website, social, ads)</li>
</ul>
<p>These efforts help the app reach more downloads and active users.</p>

<h2>Conclusion and Next Steps</h2>
<p><strong>Publishing an app on the App Store</strong> requires proper planning, technical preparation and policy compliance. Creating an <strong>Apple Developer account</strong>, preparing the app according to guidelines, entering information in App Store Connect and uploading a build via Xcode for review are the core steps. A compliant, high-quality <strong>iOS app development</strong> process makes review smoother and increases the app's chances of success in the store.</p>
<p><strong>Take action:</strong> For support with developing or publishing your iOS app, reach out via our <a href="/en/contact/">contact</a> page or explore our <a href="/en/mobile-app/">mobile app development</a> services.</p>

<h2>Frequently Asked Questions</h2>

<h3>Is it free to upload an app to the App Store?</h3>
<p>No. You need an Apple Developer Program membership to publish on the App Store; the membership costs 99 USD per year. You cannot submit apps without it.</p>

<h3>How long does App Store review take?</h3>
<p>Usually 1–3 business days. It can be longer during busy periods or if information is missing or the app does not comply. The result is sent by email.</p>

<h3>Can any app be published on the App Store?</h3>
<p>No. Apps that do not follow Apple's Human Interface, Privacy and Content guidelines can be rejected. It is best to read the guidelines and prepare your app accordingly.</p>

<h3>Is TestFlight beta testing required?</h3>
<p>No, but it is recommended. With TestFlight you can test on real devices, find issues before review and improve the user experience.</p>"""


def add_blog_post(apps, schema_editor):
    BlogPost = apps.get_model('main', 'BlogPost')
    if BlogPost.objects.filter(slug='app-store-uygulama-yayinlama-rehberi').exists():
        return
    BlogPost.objects.create(
        title='App Store\'a Uygulama Yayınlama Rehberi',
        title_en='How to Publish an App on the App Store',
        slug='app-store-uygulama-yayinlama-rehberi',
        slug_en='how-to-publish-an-app-on-app-store',
        category='Mobile App',
        tags='app store uygulama yayınlama, ios uygulama yayınlama, apple developer hesabı, app store uygulama yükleme, ios uygulama geliştirme',
        excerpt='App Store\'a uygulama nasıl yüklenir? Apple Developer hesabı açma, Xcode ile yükleme ve App Store inceleme süreci hakkında detaylı rehber.',
        excerpt_en='Learn how to publish an app on the Apple App Store step by step including developer account setup, app upload and review process.',
        content=build_content_tr(),
        content_en=build_content_en(),
        published=True,
        published_at=timezone.now(),
        featured=False,
    )


def remove_blog_post(apps, schema_editor):
    BlogPost = apps.get_model('main', 'BlogPost')
    BlogPost.objects.filter(slug='app-store-uygulama-yayinlama-rehberi').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_add_blog_mobile_app_ux_mistakes'),
    ]

    operations = [
        migrations.RunPython(add_blog_post, remove_blog_post),
    ]
