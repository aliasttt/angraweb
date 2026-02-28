from __future__ import annotations

import random
from typing import Dict, List, Tuple

from django.utils import timezone

from ..models import SeoPage
from ..silo_config import SERVICE_SILO_MAP
from .utils import MetaPack, cta_box, faq, h2, h3, make_meta, p, ul, word_count_from_html, clamp_text

# IMPORTANT (validation): Non-pricing pages must NOT use in content_html:
# TR: fiyat, maliyet, ücret, paket — use neutral wording (e.g. bütçe, kapsam, tarife sayfası → kapsam sayfası).

def _service_name(page: SeoPage) -> str:
    return page.service.tr_name


def _service_base(page: SeoPage) -> str:
    return page.service.tr_base_path


def _pillar_url(page: SeoPage) -> str:
    return f"/tr/{_service_base(page)}/"


def _web_design_pillar_tr(page: SeoPage) -> Dict:
    """Custom SEO pillar content for Web Tasarım (TR) — topical authority, internal links, FAQ."""
    body: List[str] = []

    # H1 is shown in template as page.title
    body.append(
        p(
            "Web tasarım yalnızca \"güzel görünüm\" değildir; performans (Core Web Vitals), teknik SEO, UI/UX, güvenlik ve dönüşüm odaklı yapı "
            "birlikte çalıştığında gerçek sonuç verir. Angraweb olarak İstanbul'da işletmeler için mobil uyumlu, hızlı ve ölçülebilir web siteleri geliştiriyoruz."
        )
    )

    body.append(h2("Genel bakış"))
    body.append(
        p(
            "Bu sayfa, web tasarım hizmetlerimizin kapsamını ve çalışma yaklaşımımızı net bir çerçeveyle sunar. "
            "Buradaki amaç: doğru beklentiyi kurmak ve projenizi sürpriz revizyonlar yerine ölçülebilir teslim kriterleri ile ilerletmektir."
        )
    )
    body.append(p("Bu sayfadan:"))
    body.append(
        ul(
            [
                "Hangi yaklaşımın size uygun olduğunu,",
                "Proje süreci ve teslimatların nasıl planlandığını,",
                "SEO + performans + UX + güvenlik standartlarını,",
                "Kapsam ve teklifin nasıl netleştiğini görebilirsiniz.",
            ]
        )
    )
    body.append(
        p(
            "Hızlı ilerlemek isterseniz: "
            f"{{{{ link:{_quote_url(page)} }}}}, "
            f"{{{{ link:{_pricing_url(page)} }}}} ve "
            f"{{{{ link:{_guide_url(page)} }}}} bölümlerini kullanın."
        )
    )

    body.append(h2("Hangi ihtiyaca hangi yaklaşım uygundur?"))
    body.append(
        p(
            "Başarılı projeler genellikle aynı sırayı takip eder: hedef → kullanıcı → içerik/mimari → tasarım → geliştirme → test → yayın → ölçümleme. "
            "Aşağıdaki 3 senaryo doğru yaklaşımı seçmenize yardımcı olur."
        )
    )

    body.append(h3("1) Kurumsal görünürlük + güven (Kurumsal site)"))
    body.append(
        p(
            "Marka algısı, itibar ve temel lead toplama hedefleniyorsa "
            f"{{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}} yaklaşımı uygundur. "
            "Özellikle İstanbul'da hizmet veren işletmelerde; hızlı yüklenen sayfalar, net CTA'lar ve teknik SEO temel fark yaratır. "
            f"İlgili: {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}, {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi-yaptirmak/ }}}}"
        )
    )

    body.append(h3("2) Ölçek + entegrasyon + özel ihtiyaç (Özel yazılım)"))
    body.append(
        p(
            "CRM/ERP entegrasyonu, özel modüller, rol bazlı yetki, çoklu dil/çoklu şube gibi ihtiyaçlar varsa "
            f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}} gerekir. "
            "Bu durumda hazır tema sınırları yerine modüler mimari, API entegrasyonları, güvenlik sertleştirmesi ve sürdürülebilir bakım planı önemlidir. "
            f"İlgili: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}, {{{{ link:/tr/web-tasarim/django-web-gelistirme/ }}}}"
        )
    )

    body.append(h3("3) Bütçe/süre baskısı (Hazır altyapı vs özel geliştirme)"))
    body.append(
        p(
            "Hızlı yayın ve düşük başlangıç bütçesi öncelikse hazır altyapılar mantıklı olabilir; ancak ölçek büyüdükçe sınırlara takılabilirsiniz. "
            "Bu yüzden karar verirken \"bugün\" değil, 6–12 ay sonraki ihtiyaçları da düşünün."
        )
    )
    body.append(p(f"İlgili: {{{{ link:/tr/web-tasarim/ozel-yazilim-vs-hazir-site/ }}}}"))

    body.append(h2("Süreç ve teslimatlar"))
    body.append(p("Şeffaf süreç, teslim kalitesini artırır. Bizim standart akışımız:"))

    body.append(h3("1) Keşif & Brief (1–3 gün)"))
    body.append(
        ul(
            [
                "Hedefler: satış/lead, marka, operasyonel verimlilik",
                "Kullanıcı profili ve kritik akışlar",
                "Rakip & referans inceleme",
                "Kapsam taslağı ve öncelikler",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> Brief özeti + ilk kapsam taslağı"))

    body.append(h3("2) Bilgi mimarisi & içerik planı (3–7 gün)"))
    body.append(
        ul(
            [
                "Sayfa hiyerarşisi (pillar/cluster)",
                "Menü, iç bağlantı planı, içerik şablonları",
                "SEO başlık yapısı (H1/H2), schema planı",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> Sayfa mimarisi + içerik şablonları"))

    body.append(h3("3) UI/UX & Tasarım sistemi (1–2 hafta)"))
    body.append(
        ul(
            [
                "Responsive tasarım (mobil-first)",
                "Bileşen kütüphanesi (butonlar, kartlar, formlar)",
                "Kullanıcı deneyimi: okunabilirlik, görsel hiyerarşi, CTA yerleşimi",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> Tasarım sistemi + ana ekran tasarımları"))

    body.append(h3("4) Geliştirme (1–3 hafta)"))
    body.append(
        ul(
            [
                "Performans optimizasyonu, görsel optimizasyon, cache stratejileri",
                "Teknik SEO: meta, canonical, robots, sitemap, schema markup",
                "Güvenlik: HTTPS, temel sertleştirme, yetkiler",
                "Formlar: lead toplama, spam koruması",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> Çalışan site + yönetim alanı (gerekiyorsa)"))

    body.append(h3("5) Test & Yayın (2–5 gün)"))
    body.append(
        ul(
            [
                "Core Web Vitals kontrolü",
                "Kırık link, yönlendirme, form testleri",
                "Analytics/etiketleme kontrolü",
                "Yayın checklist + geri dönüş planı",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> Yayın raporu + kontrol listesi"))

    body.append(h2("Kalite standartları"))
    body.append(
        p("Kaliteyi \"hissiyat\" değil, ölçülebilir hedeflerle yönetiyoruz:")
    )
    body.append(h3("Performans (Core Web Vitals)"))
    body.append(p("Hızlı açılış, optimize görseller, doğru cache. Mobilde gerçek kullanıcı deneyimine odak."))
    body.append(h3("Teknik SEO + Schema"))
    body.append(
        p(
            "SEO uyumlu başlık hiyerarşisi, schema markup (Organization, FAQ, Breadcrumb vb.), iç bağlantı stratejisi (topic cluster)."
        )
    )
    body.append(h3("UI/UX + Erişilebilirlik"))
    body.append(
        p(
            "Mobil uyumlu (responsive). Kontrast, font, buton boyutları. Temel WCAG prensiplerine uyum."
        )
    )
    body.append(h3("Güvenlik + KVKK (genel)"))
    body.append(
        p(
            "HTTPS, güvenli form akışları. Rol/yetki yaklaşımı (varsa yönetim panelinde). Gizlilik politikası & çerez yaklaşımı."
        )
    )
    body.append(h3("Ölçümleme (Analytics)"))
    body.append(
        p(
            "Lead form dönüşümleri, temel event tracking (tıklamalar, CTA). İlk 30 gün iyileştirme listesi."
        )
    )

    body.append(h2("Bilgi mimarisi ve iç bağlantı yaklaşımı (Pillar/Cluster)"))
    body.append(
        p(
            "Arama motorları ve kullanıcılar, konuları ilişkilendiren siteleri daha iyi anlar. Bu yüzden: "
            "<strong>Pillar:</strong> Web tasarım ana çerçevesi (bu sayfa). "
            "<strong>Cluster:</strong> tek bir soruyu derinlemesine çözen sayfalar. "
            "Planlı iç link: cluster → pillar, pillar → cluster."
        )
    )
    body.append(p("İlgili konular:"))
    body.append(
        ul(
            [
                f"{{{{ link:/tr/web-tasarim/ajans-mi-freelancer-mi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/web-tasarim-freelancer/ }}}}",
                f"{{{{ link:/tr/web-tasarim/web-tasarim-sirketi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/profesyonel-web-tasarim/ }}}}",
                f"{{{{ link:/tr/web-tasarim/web-developer-istanbul/ }}}}",
                f"{{{{ link:/tr/web-tasarim/istanbul/ }}}}",
                f"{{{{ link:/tr/web-tasarim/django-vs-php/ }}}}",
                f"{{{{ link:/tr/web-tasarim/django-web-gelistirme/ }}}}",
            ]
        )
    )

    body.append(h2("Teklif & kapsam nasıl netleşir?"))
    body.append(p("Teklifin doğru çıkması için 1 sayfalık kısa brif yeter:"))
    body.append(h3("Zorunlu bilgiler"))
    body.append(
        ul(
            [
                "İş hedefi (lead/satış/marka)",
                "Hedef kitle ve hizmet bölgesi (İstanbul / Türkiye)",
                "İstenen sayfalar + kritik akışlar (form, WhatsApp, arama vb.)",
                "Dil(ler) ve içerik durumu",
                "Örnek alınan 2–3 referans site",
            ]
        )
    )
    body.append(h3("Opsiyonel"))
    body.append(
        ul(
            [
                "Entegrasyon (CRM, ödeme, randevu)",
                "Blog/rehber planı",
                "Bakım & destek ihtiyacı",
            ]
        )
    )

    body.append(
        cta_box(
            "Teklif Al",
            "Hedefinizi 2–3 cümleyle paylaşın; size uygun kapsamı ve planı hızlıca çıkaralım.",
            _quote_url(page),
            "Teklif almak için formu doldurun.",
            strong=True,
        )
    )
    body.append(h3("Neler kazanırsınız"))
    body.append(
        ul(
            [
                "Mobil uyumlu, hızlı web sitesi (Core Web Vitals odaklı)",
                "Teknik SEO temeli + schema markup",
                "Dönüşüm odaklı yapı (CTA + lead toplama)",
                "Sürdürülebilir bakım yaklaşımı",
            ]
        )
    )
    body.append(
        p(
            f"İlgili: {{{{ link:{_quote_url(page)} }}}}, "
            f"{{{{ link:{_pricing_url(page)} }}}}, "
            f"{{{{ link:{_guide_url(page)} }}}}"
        )
    )

    content_html = "\n".join(body)

    faq_pairs = [
        (
            "Web tasarım süresi neye göre değişir?",
            "Kapsam (sayfa sayısı, içerik, entegrasyon) ve onay hızına göre değişir. Net teslim kriterleri süreyi öngörülebilir yapar.",
        ),
        (
            "SEO uyumlu web sitesi tam olarak ne demek?",
            "Teknik SEO altyapısı (meta, sitemap, schema, hız), doğru içerik mimarisi ve iç link planı demektir.",
        ),
        (
            "Hazır site mi özel yazılım mı seçmeliyim?",
            "Bütçe/süre kısa ise hazır altyapı; entegrasyon ve ölçek hedefiniz varsa özel yazılım daha uygundur.",
        ),
        (
            "İstanbul'da yerinde görüşme yapıyor musunuz?",
            "İstanbul içi uygun durumlarda kısa keşif görüşmesi yapılabilir; süreç uzaktan da yönetilebilir.",
        ),
        (
            "Django ile web geliştirme hangi projelerde mantıklı?",
            "Özel modül, kullanıcı rolleri, entegrasyon ve ölçek ihtiyacı olan projelerde güçlü bir seçenektir.",
        ),
        (
            "Yayından sonra bakım ve destek var mı?",
            "Evet. Güncelleme, güvenlik, performans ve küçük iyileştirmeler için bakım modeli sunulur.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Tasarım (İstanbul) | SEO Uyumlu, Hızlı ve Dönüşüm Odaklı"
    meta_description = (
        "İstanbul merkezli web tasarım ve geliştirme: mobil uyumlu, Core Web Vitals odaklı, "
        "teknik SEO + UI/UX ile dönüşüm getiren web siteleri."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Tasarım — Genel Bakış",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_kurumsal_web_sitesi_tr(page: SeoPage) -> Dict:
    """Custom cluster: Kurumsal Web Sitesi — commercial investigation + service authority. 900–1200 words."""
    body: List[str] = []

    body.append(h2("Kurumsal Web Sitesi Nedir?"))
    body.append(
        p(
            "Kurumsal web sitesi, işletmenizin dijital yüzü olarak marka otoritesini, güveni ve dönüşüm hedeflerini tek bir çatı altında toplar. "
            "Yalnızca bilgi vermekle kalmaz; ziyaretçiyi lead veya satışa yönlendiren, mobil uyumlu ve arama motorlarında görünür bir profesyonel web sitesi, "
            "özellikle KOBİ ve B2B firmaları için rekabet avantajı sağlar."
        )
    )
    body.append(
        p(
            "Doğru kurgulandığında kurumsal site, hem itibar hem de ölçülebilir sonuçlar üretir: form doldurma, iletişim talepleri ve temel analitik verileri "
            "tek bir platformda toplanır. Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Neden SEO Uyumlu Kurumsal Web Tasarım Önemlidir?"))
    body.append(
        p(
            "SEO uyumlu kurumsal web tasarım, görünürlük ve kullanılabilirliği bir araya getirir. "
            "Teknik SEO (meta yapısı, sitemap, canonical), Core Web Vitals ile hızlı açılış, mobil uyumlu (responsive) yapı ve net kullanıcı deneyimi; "
            "arama sıralaması ve dönüşüm oranını doğrudan etkiler. Schema markup (Organization, FAQ, Breadcrumb) ile arama sonuçlarında zengin snippet desteği sağlanır."
        )
    )
    body.append(
        p(
            "Google ve diğer arama motorları, sayfa hızı, mobil uyum ve içerik yapısını sıralama sinyali olarak kullanır. "
            "Bu nedenle kurumsal site yaptırmak isteyen işletmeler için teknik temel, uzun vadeli organik trafik için belirleyicidir."
        )
    )
    body.append(
        ul(
            [
                "Teknik SEO: başlık hiyerarşisi, iç bağlantı, indekslenebilirlik",
                "Core Web Vitals: LCP, FID, CLS odaklı performans",
                "Mobil uyum: tüm cihazlarda tutarlı deneyim",
                "Kullanıcı deneyimi: okunabilirlik, CTA yerleşimi, form akışları",
                "Schema markup: yapılandırılmış veri ile görünürlük",
            ]
        )
    )

    body.append(h2("İstanbul'da Kurumsal Web Sitesi Yaptırmak"))
    body.append(
        p(
            "İstanbul merkezli hizmet veren işletmeler için kurumsal web sitesi, hem yerel hem ulusal hedef kitleye ulaşmanın temelidir. "
            "İstanbul Avrupa Yakası ve Anadolu Yakası’ndaki firmalarla yüz yüze keşif görüşmeleri mümkündür; Türkiye genelinde ise uzaktan süreç yönetimi ile aynı kalite sunulur."
        )
    )
    body.append(
        p(
            "Yerel arama (yerel SEO) ve \"İstanbul kurumsal web tasarım\" arayan işletmeler için site yapısı ve iletişim bilgileri tutarlı biçimde sunulur. "
            f"Yerel hizmet detayları için {{{{ link:/tr/web-tasarim/istanbul/ }}}} sayfasını inceleyebilirsiniz."
        )
    )

    body.append(h2("Kurumsal Web Sitesi Süreci"))
    body.append(
        p(
            "Standart teslimat akışı: keşif ve hedef netleştirme, bilgi mimarisi ve sayfa planı, UI/UX tasarım (mobil öncelikli), "
            "geliştirme (gerektiğinde Django tabanlı altyapı), test ve yayın. Her aşamada teslim çıktıları ve kabul kriterleri yazılıdır."
        )
    )
    body.append(
        ul(
            [
                "Keşif: hedef kitle, rakipler, dönüşüm noktaları",
                "Bilgi mimarisi: sayfa hiyerarşisi, menü, içerik planı",
                "UI/UX tasarım: bileşen kütüphanesi, responsive ekranlar",
                "Geliştirme: performans, teknik SEO, güvenlik (HTTPS); gerekiyorsa Django ile ölçeklenebilir yapı",
                "Test ve yayın: Core Web Vitals, form ve link kontrolleri",
            ]
        )
    )
    body.append(
        p(
            "Daha karmaşık entegrasyon veya özel modüller (CRM, çoklu dil, rol bazlı yetkiler) gerekiyorsa "
            f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}} yaklaşımı uygundur."
        )
    )

    body.append(h2("Hangi İşletmeler İçin Uygundur?"))
    body.append(
        p(
            "Kurumsal web sitesi çözümü; KOBİ’ler, B2B firmaları, ajanslar, danışmanlar ve büyümekte olan şirketler için uygundur. "
            "Temel ihtiyaç: marka algısını güçlendirmek, lead toplamak ve dijital varlığı tek bir adreste profesyonelce sunmaktır."
        )
    )
    body.append(
        ul(
            [
                "KOBİ’ler ve yerel/ulusal hedefli firmalar",
                "B2B satış ve kurumsal iletişim odaklı şirketler",
                "Ajanslar ve danışmanlık ofisleri",
                "Büyüme aşamasındaki girişimler",
            ]
        )
    )

    body.append(h2("Kurumsal Web Sitesi ile Neler Kazanırsınız?"))
    body.append(
        p(
            "Yatırımın geri dönüşü; güven, lead artışı ve marka konumlandırma ile ölçülebilir hale gelir. "
            "Analitik ve dönüşüm takibi sayesinde hangi sayfaların ve CTA'ların işe yaradığı netleşir."
        )
    )
    body.append(
        ul(
            [
                "Güven: tutarlı marka dili ve güvenli (HTTPS) altyapı",
                "Lead artışı: form, WhatsApp ve CTA odaklı dönüşüm noktaları",
                "Marka konumlandırma: rakiplerden ayrışan profesyonel görünüm",
                "Ölçülebilir performans: analitik ve Core Web Vitals ile iyileştirme imkânı",
            ]
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/istanbul/ }}}}",
            ]
        )
    )

    body.append(h2("Kurumsal sitede olmazsa olmazlar"))
    body.append(
        p(
            "Profesyonel kurumsal web sitesi; hızlı yüklenme, mobil uyumluluk, net iletişim ve teklif/iletişim formu ile tamamlanır. "
            "Güvenlik için HTTPS, erişilebilirlik için temel kontrast ve font seçimi, dönüşüm için ise az sayıda ancak net CTA önerilir."
        )
    )
    body.append(
        ul(
            [
                "Hız ve Core Web Vitals uyumu",
                "Mobil uyumlu (responsive) tüm sayfalar",
                "İletişim formu ve/veya WhatsApp / arama butonu",
                "HTTPS ve güncel güvenlik ayarları",
                "Temel analitik ve dönüşüm takibi",
            ]
        )
    )

    body.append(
        cta_box(
            "Teklif Al",
            "Kurumsal web sitenizin kapsamını netleştirmek için hedeflerinizi paylaşın; size uygun planı birlikte çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)

    faq_pairs = [
        (
            "Kurumsal web sitesi ne kadar sürede teslim edilir?",
            "Kapsam (sayfa sayısı, içerik, entegrasyon) ve onay hızına göre değişir. Net teslim kriterleri ile süre öngörülebilir hale gelir.",
        ),
        (
            "SEO uyumlu kurumsal web sitesi ne demek?",
            "Teknik SEO altyapısı (meta, sitemap, schema, hız), mobil uyum ve içerik mimarisi ile arama motorlarında görünür, kullanıcı odaklı site demektir.",
        ),
        (
            "İstanbul dışından da hizmet alınabilir mi?",
            "Evet. Türkiye genelinde uzaktan süreç yönetimi ile çalışıyoruz; İstanbul içi gerektiğinde yüz yüze keşif yapılabilir.",
        ),
        (
            "Kurumsal site ile özel yazılım arasındaki fark nedir?",
            "Kurumsal site genelde sabit sayfa seti ve temel form/lead akışı içerir. CRM/ERP entegrasyonu, özel modüller veya çoklu dil/şube gerekiyorsa özel yazılım yaklaşımı uygundur.",
        ),
        (
            "Yayından sonra bakım sunuluyor mu?",
            "Evet. Güncelleme, güvenlik ve performans iyileştirmeleri için bakım ve destek modeli sunulur.",
        ),
        (
            "Hangi bilgilerle teklif alabilirim?",
            "Hedef, hedef kitle, örnek referans siteler ve istenen sayfalar/akışlar yeterlidir. Kısa brif ile hızlıca yanıt verilir.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Kurumsal Web Sitesi | SEO Uyumlu, Mobil Uyumlu — İstanbul"
    meta_description = (
        "İstanbul merkezli kurumsal web tasarım: SEO uyumlu, mobil uyumlu, dönüşüm odaklı kurumsal site. "
        "Profesyonel çözümler ve yerel hizmet."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Kurumsal Web Sitesi — Profesyonel ve SEO Uyumlu Çözümler",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_ajans_mi_freelancer_mi_tr(page: SeoPage) -> Dict:
    """Custom cluster: Ajans mı Freelancer mı? — long-form SEO, 1100+ words. No pricing triggers in body."""
    body: List[str] = []

    body.append(
        p(
            "Web tasarım yaptırmak isteyen işletmelerin en sık sorduğu soru: ajans mı freelancer mı? "
            "Bu karar sadece bütçeyle ilgili değildir. SEO uyumluluk, teknik performans, süreç yönetimi ve uzun vadeli ölçeklenebilirlik açısından ciddi farklar vardır."
        )
    )
    body.append(
        p(
            "Google'da rekabetin arttığı bir dönemde; web tasarım ajansı ile freelancer web tasarımcı arasında seçim yaparken teknik SEO, Core Web Vitals, "
            "mobil uyumluluk ve dönüşüm optimizasyonu gibi kriterler dikkate alınmalıdır. "
            f"Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Web Tasarım Ajansı Nedir?"))
    body.append(
        p(
            "Web tasarım ajansı; tasarımcı, geliştirici, SEO uzmanı ve proje yöneticisinden oluşan ekip yapısıyla çalışır. "
            "Profesyonel web tasarım projelerinde süreç planlı ilerler."
        )
    )
    body.append(h3("Avantajları"))
    body.append(
        ul(
            [
                "Teknik SEO uzmanlığı",
                "Core Web Vitals optimizasyonu",
                "İç bağlantı stratejisi (topic cluster)",
                "Ölçeklenebilir altyapı",
                "Entegrasyon yönetimi",
                "Süreç ve raporlama disiplini",
            ]
        )
    )
    body.append(
        p(
            "İstanbul web tasarım ajansları özellikle rekabetin yüksek olduğu sektörlerde SEO uyumlu web sitesi geliştirme konusunda avantaj sağlar."
        )
    )

    body.append(h2("Freelancer Web Tasarımcı Nedir?"))
    body.append(
        p(
            "Freelancer web tasarımcı; projeyi tek başına yöneten bağımsız uzmandır."
        )
    )
    body.append(h3("Avantajları"))
    body.append(
        ul(
            [
                "Esnek iletişim",
                "Küçük projelerde hızlı başlangıç",
                "Basit kurumsal web sitelerinde yeterli çözüm",
            ]
        )
    )
    body.append(
        p(
            "Ancak teknik SEO, güvenlik sertleştirme, performans optimizasyonu ve uzun vadeli geliştirme gereksinimlerinde tek kişinin uzmanlığı sınırlı olabilir. "
            f"Freelancer ile çalışma detayları: {{{{ link:/tr/web-tasarim/web-tasarim-freelancer/ }}}}."
        )
    )

    body.append(h2("SEO Açısından Ajans mı Freelancer mı?"))
    body.append(
        p(
            "SEO uyumlu web sitesi yalnızca meta tag eklemek değildir. Gerçek SEO şunları içerir: teknik SEO altyapısı, schema markup, site mimarisi (pillar + cluster), "
            "iç link stratejisi, mobil-first tasarım, Core Web Vitals optimizasyonu, crawl budget yönetimi."
        )
    )
    body.append(
        p(
            "Ajans modelinde bu alanlar ekip çalışmasıyla yürütülür. Freelancer modelinde ise tüm sorumluluk tek kişidedir. "
            "Rekabetin yoğun olduğu İstanbul gibi pazarlarda SEO stratejik yaklaşım gerektirir."
        )
    )

    body.append(h2("Performans ve Core Web Vitals"))
    body.append(
        p(
            "Google sıralamalarında hız kritik faktördür. Önemli metrikler: LCP (Largest Contentful Paint), CLS (Cumulative Layout Shift), INP / Interaction latency, mobil performans."
        )
    )
    body.append(
        p(
            "Ajans projelerinde genellikle görsel optimizasyon, cache stratejileri, minimal JS kullanımı, backend sorgu optimizasyonu, CDN yapılandırması planlı yapılır. "
            "Freelancer projelerinde bu optimizasyon seviyesi kişisel bilgiye bağlıdır."
        )
    )

    body.append(h2("Ölçeklenebilirlik"))
    body.append(
        p(
            "Proje büyüdüğünde ihtiyaçlar değişir: çoklu dil, çoklu şube, CRM entegrasyonu, özel yazılım modülleri, API bağlantıları. "
            "Bu noktada modüler mimari gerekir. "
            f"Özel yazılım web sitesi projelerinde ajans yapısı genellikle daha sürdürülebilir olur: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Süreç Yönetimi ve Risk Kontrolü"))
    body.append(
        p(
            "Profesyonel web tasarım projelerinde süreç şunları içerir: keşif ve brief, bilgi mimarisi, UI/UX tasarım, geliştirme, test ve yayın, ölçümleme. "
            "Ajans yapısında bu adımlar dokümante edilir. Freelancer projelerinde süreç daha esnek ilerler."
        )
    )
    body.append(
        p(
            f"Adım adım yaklaşım için {{{{ link:{_guide_url(page)} }}}} rehberini inceleyebilirsiniz."
        )
    )

    body.append(h2("Hangi Durumda Freelancer Mantıklı?"))
    body.append(
        ul(
            [
                "Tek sayfa landing page",
                "Basit kurumsal site",
                "Kısa süreli proje",
                "Düşük entegrasyon ihtiyacı",
            ]
        )
    )

    body.append(h2("Hangi Durumda Ajans Daha Doğru?"))
    body.append(
        ul(
            [
                "SEO odaklı büyüme hedefi",
                "Kurumsal web sitesi",
                "E-ticaret projesi",
                "Özel yazılım geliştirme",
                "Uzun vadeli dijital strateji",
            ]
        )
    )

    body.append(h2("İstanbul'da Web Tasarım Seçimi"))
    body.append(
        p(
            "İstanbul web tasarım rekabeti yüksektir. Google'da görünür olmak için teknik SEO, içerik stratejisi ve performans birlikte çalışmalıdır. "
            "Bu nedenle seçim yaparken: uzmanlık alanı, süreç şeffaflığı, SEO yaklaşımı, ölçeklenebilirlik planı değerlendirilmelidir."
        )
    )
    body.append(
        p(
            f"Yerel hizmet: {{{{ link:/tr/web-tasarim/istanbul/ }}}}. "
            f"Kurumsal site karşılaştırması: {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Freelancer esneklik sunar. Ajans sistem ve ölçek sunar. SEO, teknik yapı ve uzun vadeli büyüme hedefleniyorsa; planlı ve performans odaklı yaklaşım daha güvenlidir."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/web-tasarim-freelancer/ }}}}",
                f"{{{{ link:/tr/web-tasarim/web-tasarim-sirketi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/istanbul/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Ajans veya freelancer kararını birlikte netleştirmek için hedeflerinizi paylaşın; size uygun modeli önerelim.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)

    faq_pairs = [
        ("Ajans ile freelancer arasındaki temel fark nedir?", "Ajans ekip yapısı, süreç ve raporlama sunar; freelancer tek kişiyle esnek iletişim sağlar. SEO ve ölçek ihtiyacı yüksekse ajans genelde daha uygundur."),
        ("SEO için ajans mı freelancer mı tercih edilmeli?", "Teknik SEO, Core Web Vitals ve iç bağlantı stratejisi ekip bilgisi gerektirir. Rekabetçi anahtar kelimelerde ajans yaklaşımı daha güvenlidir."),
        ("Freelancer ne zaman yeterli olur?", "Tek sayfa, basit kurumsal site veya düşük entegrasyon ihtiyacında freelancer mantıklı olabilir."),
        ("İstanbul'da ajans seçerken nelere dikkat etmeli?", "Uzmanlık alanı, süreç şeffaflığı, SEO yaklaşımı ve ölçeklenebilirlik planı değerlendirilmeli."),
        ("Ölçek büyüdüğünde ne yapılmalı?", "Çoklu dil, CRM veya özel modül ihtiyacı doğarsa modüler altyapı ve ajans/ekip modeli daha sürdürülebilirdir."),
        ("Teklif almak için hangi bilgiler gerekli?", "Hedef, kapsam ve tercih (ajans / freelancer / kararsız) paylaşmanız yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Ajans mı Freelancer mı? Web Tasarım İçin Hangisi Daha Doğru?"
    meta_description = (
        "Web tasarım ajansı mı freelancer mı? SEO, performans, süreç yönetimi ve ölçeklenebilirlik açısından detaylı karşılaştırma rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Ajans mı Freelancer mı? Web Tasarım İçin Doğru Seçim",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_django_vs_php_tr(page: SeoPage) -> Dict:
    """Custom cluster: Django ve PHP Karşılaştırması — comparison + technical authority. No pricing triggers."""
    body: List[str] = []

    body.append(
        p(
            "Web geliştirme projelerinde en sık karşılaştırılan iki teknoloji: Django ve PHP. "
            "Her ikisi de güçlüdür; ancak mimari yaklaşım, güvenlik modeli, performans yönetimi ve SEO altyapısı açısından ciddi farklar bulunur."
        )
    )
    body.append(
        p(
            "Bu rehberde Django ve PHP'yi teknik düzeyde karşılaştırıyoruz. "
            f"Genel web tasarım çerçevesi için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Django Nedir?"))
    body.append(
        p(
            "Django; Python tabanlı, yüksek güvenlikli ve modüler yapıya sahip bir web framework'üdür. "
            "Büyük ölçekli projelerde tercih edilir ve özellikle özel yazılım web sitesi projelerinde güçlü altyapı sunar."
        )
    )
    body.append(
        ul(
            [
                "MVC benzeri MVT mimarisi",
                "Dahili admin panel",
                "ORM (veritabanı soyutlama)",
                "Güçlü güvenlik mekanizmaları",
                "Modüler uygulama yapısı",
                "SEO dostu URL kontrolü",
            ]
        )
    )

    body.append(h2("PHP Nedir?"))
    body.append(
        p(
            "PHP; web geliştirme dünyasında uzun yıllardır kullanılan sunucu taraflı programlama dilidir. "
            "Birçok hazır altyapı ve CMS sistemi PHP üzerine kuruludur."
        )
    )
    body.append(
        p(
            "Avantajları: geniş ekosistem, çok sayıda hazır sistem, hızlı başlangıç. "
            "Ancak framework kullanılmadan yazılan PHP projelerde kod standardı ve güvenlik kişisel deneyime bağlıdır."
        )
    )

    body.append(h2("Mimari Karşılaştırma"))
    body.append(
        p(
            "Django: standart proje yapısı, temiz uygulama modülleri, ayrılmış katman mimarisi, test yazımı kolay. "
            "PHP: framework kullanılmazsa düzensiz yapı oluşabilir; kod organizasyonu geliştiriciye bağlı."
        )
    )
    body.append(
        p(
            "Kurumsal projelerde sürdürülebilirlik açısından mimari disiplin önemlidir. "
            f"Django ile web geliştirme detayları: {{{{ link:/tr/web-tasarim/django-web-gelistirme/ }}}}."
        )
    )

    body.append(h2("Güvenlik"))
    body.append(
        p(
            "Django: CSRF koruması dahili, XSS koruma mekanizması, SQL injection koruması, güvenli session yönetimi. "
            "PHP: güvenlik büyük ölçüde geliştirici pratiğine bağlıdır; framework kullanılmazsa manuel koruma gerekir."
        )
    )
    body.append(
        p(
            "Güvenlik özellikle SEO açısından önemlidir çünkü hacklenen siteler arama motorları tarafından cezalandırılabilir."
        )
    )

    body.append(h2("SEO Altyapısı"))
    body.append(
        p(
            "Django: URL yapısı tam kontrol edilebilir, dinamik sitemap üretilebilir, canonical ve hreflang yönetimi kolay, schema markup entegrasyonu rahat. "
            "PHP projelerde SEO altyapısı kullanılan framework veya CMS'e göre değişir."
        )
    )
    body.append(
        p("Teknik SEO gereksinimi yüksek projelerde Django avantaj sağlar.")
    )

    body.append(h2("Performans ve Ölçeklenebilirlik"))
    body.append(
        p(
            "Django: cache sistemleri, ORM optimizasyonu, modüler ölçekleme, API-first mimari. "
            "Yüksek trafikli projelerde daha stabil yapı sunar."
        )
    )

    body.append(h2("Hangi Projelerde Django Mantıklı?"))
    body.append(
        ul(
            [
                "Özel yazılım projeleri",
                "Kurumsal web siteleri",
                "Çoklu dil yapıları",
                "SEO odaklı içerik siteleri",
                "API entegrasyonlu platformlar",
            ]
        )
    )
    body.append(
        p(
            f"Özel yazılım web sitesi yaklaşımı: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Hangi Projelerde PHP Yeterli?"))
    body.append(
        ul(
            [
                "Basit içerik siteleri",
                "Küçük ölçekli projeler",
                "Hızlı başlangıç gerektiren işler",
            ]
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Django; güvenlik, mimari disiplin ve SEO kontrolü açısından daha yapılandırılmış bir framework'tür. "
            "PHP ise geniş ekosistemi sayesinde farklı kullanım alanları sunar."
        )
    )
    body.append(
        p(
            "Özellikle teknik SEO ve ölçeklenebilir özel yazılım projelerinde Django daha sürdürülebilir bir temel sağlar."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/django-web-gelistirme/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Projeniz için Django mu PHP mi uygun, birlikte netleştirelim. Hedef ve kapsamı paylaşın; size uygun öneriyi sunalım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Django ve PHP arasındaki temel fark nedir?", "Django yapılandırılmış bir framework'tür; güvenlik ve mimari varsayılan gelir. PHP dil olarak esnektir; yapı proje veya framework'e bağlıdır."),
        ("SEO için Django mu PHP mi?", "Teknik SEO kontrolü (URL, sitemap, schema) Django'da daha doğrudan yönetilebilir. PHP'de kullanılan CMS veya framework belirleyicidir."),
        ("Hangi projelerde Django tercih edilmeli?", "Kurumsal site, özel yazılım, çoklu dil, yüksek trafik ve API entegrasyonu gereken projelerde Django güçlü bir seçenektir."),
        ("PHP ne zaman yeterli olur?", "Basit içerik siteleri, küçük ölçekli projeler ve hızlı başlangıç gerektiren işlerde PHP yaygın kullanılır."),
        ("Güvenlik açısından fark var mı?", "Django CSRF, XSS, SQL injection korumasını varsayılan sunar. PHP'de güvenlik geliştirici pratiğine ve kullanılan framework'e bağlıdır."),
        ("Teklif almak için ne paylaşmalıyım?", "Hedef, kapsam (sayfa/özellik), teknik kısıtlar ve tercih (Django / PHP / kararsız) yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Django ve PHP Karşılaştırması | Hangisi Daha Güçlü?"
    meta_description = (
        "Django ve PHP karşılaştırması: performans, güvenlik, SEO altyapısı ve ölçeklenebilirlik açısından detaylı teknik analiz."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Django ve PHP Karşılaştırması — Hangi Teknoloji Daha Güçlü?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_django_web_gelistirme_tr(page: SeoPage) -> Dict:
    """Custom cluster: Django ile Web Geliştirme — technical authority, SEO-focused. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Giriş: Backend Mimarisi Neden Kritik?"))
    body.append(
        p(
            "Modern web projelerinde yalnızca tasarım yeterli değildir. "
            "Google'ın değerlendirdiği kriterler: URL yapısı, crawl verimliliği, sunucu yanıt süresi, Core Web Vitals, iç bağlantı yapısı, schema bütünlüğü. "
            "Bu kriterlerin büyük bölümü backend mimarisi ile ilgilidir."
        )
    )
    body.append(
        p(
            "Django ile web geliştirme; teknik SEO ve performans gereksinimlerini karşılamak için güçlü bir temel sunar. "
            f"Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Django Neyi Farklı Yapıyor?"))
    body.append(
        p(
            "Django, Python tabanlı ve katmanlı mimariyi zorunlu kılan bir framework'tür."
        )
    )
    body.append(
        ul(
            [
                "Modüler uygulama yapısı",
                "ORM ile optimize veritabanı sorguları",
                "Net URL routing kontrolü",
                "Dahili admin panel",
                "Middleware tabanlı istek yönetimi",
                "Güvenli kimlik doğrulama sistemi",
            ]
        )
    )
    body.append(
        p("Bu yapı, düzensiz kod ve teknik borç oluşumunu azaltır.")
    )

    body.append(h2("Teknik SEO Açısından Django"))
    body.append(
        p("Çoğu web sitesi SEO'da mimari hatalar nedeniyle kaybeder. Django ile:")
    )
    body.append(
        ul(
            [
                "SEO uyumlu URL yapısı: anahtar kelime odaklı ve hiyerarşik URL kontrolü mümkündür.",
                "Crawl budget optimizasyonu: verimli sorgular ve temiz routing ile gereksiz crawl yükü azaltılır.",
                "Dinamik sitemap yönetimi: binlerce URL içeren projelerde ölçeklenebilir sitemap üretilebilir.",
                "Canonical ve hreflang kontrolü: çok dilli projelerde hassas SEO yönetimi sağlanır.",
                "Server-side rendering avantajı: içerik arama motorları tarafından tam olarak algılanır.",
                "Schema markup otomasyonu: içerik modeline göre dinamik yapılandırılmış veri üretilebilir.",
            ]
        )
    )

    body.append(h2("Performans ve Core Web Vitals"))
    body.append(
        p(
            "Google sıralamasında hız kritik rol oynar. Django projelerinde: sorgu optimizasyonu, cache stratejileri, minimal template yapısı, backend seviyesinde performans ayarı yapılabilir. "
            "Performans sorunları daha hızlı tespit edilir ve çözülür."
        )
    )

    body.append(h2("Güvenlik ve Uzun Vadeli SEO"))
    body.append(
        p(
            "Güvenlik açıkları SEO'yu doğrudan etkiler. Django: CSRF koruması, XSS önleme, SQL injection koruma, güvenli oturum yönetimi gibi mekanizmaları varsayılan olarak sunar. "
            "Bu da domain otoritesinin korunmasına katkı sağlar."
        )
    )

    body.append(h2("Ölçeklenebilirlik"))
    body.append(
        p(
            "Django: API-first mimari, çoklu dil sistemleri, rol bazlı yetkilendirme, CRM/ERP entegrasyonu, mikroservis genişletilebilirliği gibi büyüme senaryolarına uygundur."
        )
    )

    body.append(h2("Hangi Projelerde Django Mantıklı?"))
    body.append(
        ul(
            [
                "Kurumsal web siteleri",
                "SEO odaklı içerik platformları",
                "Özel yazılım projeleri",
                "SaaS sistemleri",
                "Entegrasyon gerektiren platformlar",
            ]
        )
    )
    body.append(
        p(
            f"Özel yazılım web sitesi: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}. "
            f"Django ve PHP karşılaştırması: {{{{ link:/tr/web-tasarim/django-vs-php/ }}}}."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Django ile web geliştirme; performans, güvenlik ve teknik SEO kontrolü açısından güçlü bir altyapı sunar. "
            "Uzun vadeli dijital büyüme hedefleyen işletmeler için backend mimarisi stratejik bir karardır."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/django-vs-php/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Django ile projenizin kapsamını netleştirmek için hedeflerinizi paylaşın; size uygun mimari önerisini sunalım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Django ile web geliştirme ne zaman tercih edilmeli?", "Teknik SEO, ölçeklenebilirlik, özel mantık ve güvenlik öncelikli projelerde Django güçlü bir seçenektir."),
        ("Django SEO açısından avantaj sağlar mı?", "Evet. URL kontrolü, sitemap, canonical/hreflang ve schema markup backend seviyesinde yönetilebilir."),
        ("Performans için Django nasıl kullanılır?", "Sorgu optimizasyonu, cache stratejileri ve backend ayarları ile Core Web Vitals hedeflenebilir."),
        ("Güvenlik Django'da nasıl?", "CSRF, XSS, SQL injection ve oturum güvenliği varsayılan mekanizmalarla sunulur."),
        ("Hangi projeler Django'ya uygun?", "Kurumsal site, içerik platformu, SaaS, entegrasyon ağırlıklı projeler Django ile uyumludur."),
        ("Teklif almak için ne gerekli?", "Hedef, kapsam ve teknik gereksinimlerinizi paylaşmanız yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Django ile Web Geliştirme | Ölçeklenebilir ve SEO Uyumlu Sistemler"
    meta_description = (
        "Django ile web geliştirme: teknik SEO altyapısı, performans optimizasyonu ve güvenli mimari ile sürdürülebilir dijital büyüme."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Django ile Web Geliştirme — Ölçeklenebilir ve SEO Odaklı Mimari",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_kurumsal_web_sitesi_yaptirmak_tr(page: SeoPage) -> Dict:
    """Custom cluster: Kurumsal Web Sitesi Yaptırmak — high-intent, decision-stage, planning guide. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kurumsal Web Sitesi Neden Sadece \"Bir Web Sitesi\" Değildir?"))
    body.append(
        p(
            "Birçok işletme kurumsal web sitesi yaptırmayı yalnızca dijital bir kartvizit olarak görür. "
            "Oysa gerçek şu: Kurumsal web sitesi; markanın güvenilirliğini, dijital görünürlüğünü ve dönüşüm potansiyelini belirleyen temel altyapıdır."
        )
    )
    body.append(
        p(
            "Yanlış planlanan bir site: Google'da görünmez, güven oluşturmaz, ölçeklenemez, teknik borç üretir. "
            "Doğru planlanan bir site ise: organik trafik üretir, marka algısını güçlendirir, satış sürecini hızlandırır, uzun vadeli dijital büyümeyi destekler."
        )
    )
    body.append(
        p(
            f"Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Kurumsal Web Sitesi Yaptırmadan Önce Sorulması Gereken Sorular"))
    body.append(
        p("Amaç nedir? Lead toplamak mı? Kurumsal itibar mı? Uluslararası görünürlük mü? Yatırımcı sunumu mu? Amaç net değilse mimari yanlış kurulur.")
    )
    body.append(
        p(
            "Hedef kitle kim? B2B mi? Son kullanıcı mı? Teknik uzman mı? Yönetici mi? "
            "Dil, içerik hiyerarşisi ve CTA yerleşimi hedef kitleye göre değişir."
        )
    )
    body.append(
        p(
            "SEO altyapısı planlandı mı? Kurumsal sitelerde en sık yapılan hata: tasarım bittikten sonra SEO düşünmek. "
            "Oysa teknik SEO şu aşamada planlanmalıdır: URL yapısı, iç link mimarisi, sayfa hiyerarşisi, schema markup, Core Web Vitals. SEO sonradan eklenmez. Başlangıçta inşa edilir."
        )
    )

    body.append(h2("Kurumsal Web Sitesinde Olması Gereken Teknik Temeller"))
    body.append(
        ul(
            [
                "Temiz URL yapısı: hiyerarşik ve anahtar kelime uyumlu.",
                "Core Web Vitals performansı: hızlı açılış, mobil uyum, stabil layout.",
                "İç bağlantı stratejisi: pillar + cluster yapısı.",
                "Structured data (schema): Organization, FAQ, Breadcrumb.",
                "Güvenlik: HTTPS, güvenli form yapısı, rol yönetimi.",
            ]
        )
    )

    body.append(h2("İstanbul'da Kurumsal Web Sitesi Yaptırmak"))
    body.append(
        p(
            "İstanbul gibi rekabetçi bir pazarda: aynı sektörde yüzlerce firma olabilir, organik sıralama rekabeti yüksektir, mobil kullanıcı oranı çok yüksektir. "
            "Bu nedenle kurumsal web tasarım yalnızca estetik değil; teknik rekabet stratejisidir."
        )
    )
    body.append(
        p(
            f"Yerel hizmet: {{{{ link:/tr/web-tasarim/istanbul/ }}}}. "
            f"Kurumsal site genel bakış: {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Hazır Sistem mi Özel Yazılım mı?"))
    body.append(
        p(
            "Hazır altyapılar hızlı başlangıç sunar ancak: URL kontrolü sınırlı olabilir, SEO esnekliği kısıtlıdır, performans optimizasyonu zorlaşabilir. "
            "Özel yazılım ise: tam teknik kontrol, modüler mimari, uzun vadeli sürdürülebilirlik sunabilir. Karar, kısa vadeli değil uzun vadeli düşünülmelidir."
        )
    )
    body.append(
        p(
            f"Özel yazılım web sitesi: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Kurumsal Web Sitesi Süreci Nasıl Olmalı?"))
    body.append(
        ul(
            [
                "Keşif ve hedef belirleme",
                "Rakip ve sektör analizi",
                "Bilgi mimarisi oluşturma",
                "UI/UX tasarım",
                "Backend geliştirme",
                "Performans optimizasyonu",
                "Test ve yayın",
                "İlk 30 gün veri analizi",
            ]
        )
    )
    body.append(p("Süreç net değilse proje dağılır."))

    body.append(h2("En Sık Yapılan Hatalar"))
    body.append(
        ul(
            [
                "SEO'yu sona bırakmak",
                "İçerik stratejisini planlamamak",
                "Performansı test etmemek",
                "Güvenliği ihmal etmek",
                "Sadece tasarıma odaklanmak",
            ]
        )
    )

    body.append(h2("Uzun Vadeli Değer"))
    body.append(
        p(
            "Kurumsal web sitesi; bir kerelik proje değildir. Düzenli güncelleme, içerik üretimi ve teknik bakım gerektirir. "
            "Gerçek değer: organik trafik artışı, marka güveni, lead kalitesi, ölçeklenebilir altyapı ile ölçülür."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Kurumsal web sitesi yaptırmak; teknik, stratejik ve uzun vadeli düşünülmesi gereken bir karardır. "
            "Başlangıçta doğru planlanan mimari; yıllarca sürdürülebilir büyüme sağlar."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/istanbul/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Kurumsal web sitenizi doğru planlamak için hedeflerinizi ve hedef kitlenizi paylaşın; size uygun yol haritasını çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Kurumsal web sitesi yaptırmadan önce ne planlanmalı?", "Amaç, hedef kitle, teknik SEO altyapısı ve süreç adımları baştan netleştirilmelidir."),
        ("SEO neden başlangıçta planlanmalı?", "URL yapısı, iç link mimarisi ve schema baştan kurulmalı; sonradan eklemek teknik borç ve kayıp görünürlük demektir."),
        ("Hazır sistem mi özel yazılım mı seçilmeli?", "Kısa vadeli hız hazır sistemde; uzun vadeli kontrol ve SEO esnekliği özel yazılımda daha güçlüdür."),
        ("İstanbul'da kurumsal site neden farklı?", "Rekabet ve mobil kullanım yüksek; teknik SEO ve performans stratejik rekabet unsuru olur."),
        ("En sık yapılan hatalar neler?", "SEO'yu sona bırakmak, içerik stratejisini planlamamak, performans ve güvenliği ihmal etmek."),
        ("Teklif almak için ne gerekli?", "Hedef, hedef kitle, örnek referanslar ve öncelikler yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Kurumsal Web Sitesi Yaptırmak | Doğru Planlama Rehberi"
    meta_description = (
        "Kurumsal web sitesi yaptırmadan önce bilmeniz gerekenler. SEO, performans, güvenlik ve uzun vadeli sürdürülebilirlik rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Kurumsal Web Sitesi Yaptırmak — Stratejik Bir Yatırım Rehberi",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_istanbul_tr(page: SeoPage) -> Dict:
    """Custom cluster: İstanbul'da Hizmet — local SEO, market insight, technical depth. No pricing triggers."""
    body: List[str] = []

    body.append(h2("İstanbul'da Dijital Rekabet Gerçekten Farklıdır"))
    body.append(
        p(
            "İstanbul, Türkiye'nin en yoğun ticari ve dijital rekabetine sahip şehridir. Aynı sektörde yüzlerce firma olabilir. Aynı anahtar kelimede onlarca rakip sıralanır."
        )
    )
    body.append(
        p(
            "Bu nedenle İstanbul'da web tasarım yaptırmak, yalnızca bir site yaptırmak değildir. Bu bir rekabet stratejisidir. "
            "Çünkü burada: küçük teknik hatalar sıralama kaybettirir, yavaş siteler mobilde elenir, SEO altyapısı zayıf olan siteler görünmez olur, içerik mimarisi zayıf olan markalar güven oluşturamaz. İstanbul pazarı hata kaldırmaz."
        )
    )
    body.append(
        p(
            f"Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("İstanbul'da Web Tasarım Neden Stratejik Planlanmalıdır?"))
    body.append(
        p(
            "Yerel rekabet, ulusal rekabetten daha serttir. Google'da \"web tasarım İstanbul\", \"kurumsal web tasarım İstanbul\", \"yazılım firması İstanbul\" gibi aramalarda: domain otoritesi yüksek firmalar, yıllardır içerik üreten ajanslar, güçlü backlink ağı olan şirketler ile yarışılır. Bu yüzden teknik altyapı başlangıçtan itibaren doğru kurulmalıdır."
        )
    )

    body.append(h2("İstanbul Odaklı SEO Yaklaşımı"))
    body.append(
        p(
            "Yerel görünürlük için yalnızca anahtar kelime eklemek yeterli değildir. Gerçek İstanbul SEO yaklaşımı şunları içerir: lokasyon odaklı URL yapısı, yerel içerik kümeleri (topic cluster), İstanbul sektörel rekabet analizi, mobil performans önceliği, harita ve konum sinyalleri, iç bağlantı hiyerarşisi. Yerel arama sonuçlarında görünürlük; teknik disiplin + doğru içerik planlaması ile mümkündür."
        )
    )

    body.append(h2("İstanbul'daki İşletmelerin En Büyük Dijital Hataları"))
    body.append(
        ul(
            [
                "Tasarımı öncelik sanmak: Estetik önemlidir, ancak Google tasarımı değil; performansı ve yapıyı değerlendirir.",
                "SEO'yu sonradan eklemek: SEO sonradan eklenmez. URL yapısı ve içerik hiyerarşisi baştan planlanmalıdır.",
                "Performansı test etmemek: Mobil kullanıcı oranı İstanbul'da çok yüksektir. Yavaş site = kaybedilen müşteri.",
                "Teknik altyapıyı hafife almak: Hazır sistemler kısa vadede hızlı olabilir. Ancak rekabetçi pazarda teknik sınırlar sorun yaratır.",
            ]
        )
    )

    body.append(h2("İstanbul'da Kurumsal Web Sitesi Yaklaşımı"))
    body.append(
        p(
            "Kurumsal firmalar için: güven veren tasarım, net mesaj, dönüşüm odaklı CTA, SEO temeli güçlü mimari, ölçeklenebilir altyapı kritiktir. İstanbul'daki B2B firmalar için özellikle teknik SEO ve içerik stratejisi belirleyicidir."
        )
    )
    body.append(
        p(
            f"Kurumsal site planlama: {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi-yaptirmak/ }}}}. "
            f"Kurumsal site genel bakış: {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Performans Neden İstanbul'da Daha Kritik?"))
    body.append(
        p(
            "İstanbul'daki kullanıcı davranışı: hızlı karar verme, mobil öncelik, alternatiflere hızlı geçiş şeklindedir. Yavaş yüklenen site, potansiyel müşteriyi rakibe yönlendirir. Core Web Vitals performansı; yalnızca sıralama değil, dönüşüm oranını da etkiler."
        )
    )

    body.append(h2("Teknik Altyapı: Yerel Rekabette Fark Yaratan Unsur"))
    body.append(
        ul(
            [
                "SEO uyumlu URL yapısı",
                "Structured data",
                "Dinamik sitemap",
                "Temiz semantik HTML",
                "Güvenli backend",
                "Ölçeklenebilir veri modeli",
            ]
        )
    )
    body.append(
        p("Teknik borç üreten projeler, 1–2 yıl içinde yeniden yapılmak zorunda kalır.")
    )

    body.append(h2("İstanbul'da Yazılım Hizmeti ve Ölçeklenebilirlik"))
    body.append(
        p(
            "Birçok firma başlangıçta küçük başlar, sonra büyür. Eğer altyapı: entegrasyona kapalıysa, veri modeli esnek değilse, API desteği yoksa, çoklu dil yapısı düşünülmemişse büyüme sınırlanır. İstanbul pazarında hızlı ölçeklenemeyen firmalar rekabette geri kalır."
        )
    )
    body.append(
        p(
            f"Özel yazılım web sitesi: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Yerel Uzmanlık Ne Sağlar?"))
    body.append(
        p(
            "İstanbul'un sektörel dağılımını bilmek: rekabet analizini doğru yapmayı, içerik tonunu doğru kurmayı, hedef kitle psikolojisini anlamayı kolaylaştırır. Yerel dinamikleri anlamayan bir yaklaşım, yüzeysel kalır."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "İstanbul'da web tasarım ve yazılım hizmeti; yalnızca teknik üretim değil, stratejik planlama gerektirir. Yerel rekabeti anlayan, teknik SEO'yu doğru kuran ve ölçeklenebilir altyapı planlayan projeler uzun vadede kazanır."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/kurumsal-web-sitesi-yaptirmak/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "İstanbul pazarında rekabetçi bir site için hedeflerinizi ve sektörünüzü paylaşın; size uygun strateji ve kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("İstanbul'da web tasarım neden farklı?", "Yerel rekabet çok yoğun; teknik hatalar ve yavaş siteler hızla sıralama kaybettirir. Stratejik planlama ve teknik SEO şarttır."),
        ("Yerel SEO için neler gerekli?", "Lokasyon odaklı URL, topic cluster, mobil performans, structured data ve iç bağlantı hiyerarşisi baştan planlanmalıdır."),
        ("En sık yapılan hatalar neler?", "Tasarıma odaklanıp SEO'yu sonraya bırakmak, performansı test etmemek, teknik altyapıyı hafife almak."),
        ("Performans neden kritik?", "İstanbul'da mobil kullanıcı oranı yüksek; yavaş site dönüşüm kaybettirir ve sıralamayı düşürür."),
        ("Ölçeklenebilirlik neden önemli?", "Firma büyüdükçe entegrasyon, API ve çoklu dil ihtiyacı doğar; altyapı buna göre planlanmalıdır."),
        ("Teklif almak için ne gerekli?", "Hedef, hedef kitle, sektör ve rakip örnekleri yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "İstanbul'da Web Tasarım ve Yazılım Hizmeti | Rekabet Odaklı Çözümler"
    meta_description = (
        "İstanbul'da SEO uyumlu, performans odaklı ve ölçeklenebilir web tasarım ve yazılım hizmeti. Yerel rekabet için stratejik yaklaşım."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "İstanbul'da Web Tasarım ve Yazılım Hizmeti — Rekabeti Anlayan Yaklaşım",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_tasarim_sirketi_tr(page: SeoPage) -> Dict:
    """Custom cluster: Web Tasarım Şirketi — professional, SEO-focused, scalable. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Web Tasarım Şirketi Seçmek Neden Kritik Bir Karardır?"))
    body.append(
        p(
            "Bir web tasarım şirketi seçmek; yalnızca bir hizmet almak değildir. "
            "Bu karar, markanızın dijital görünürlüğünü, güvenilirliğini ve uzun vadeli büyümesini doğrudan etkiler."
        )
    )
    body.append(
        p(
            "Yanlış seçilen bir web tasarım firması: SEO altyapısını zayıf kurar, performans optimizasyonunu ihmal eder, teknik borç üretir, ölçeklenebilirlik planlamaz. "
            "Doğru bir profesyonel web tasarım şirketi ise: stratejik planlama yapar, teknik SEO'yu başlangıçta kurar, performansı optimize eder, uzun vadeli sürdürülebilirlik sağlar."
        )
    )
    body.append(
        p(
            f"Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Profesyonel Web Tasarım Şirketi Neyi Farklı Yapar?"))
    body.append(
        p(
            "Birçok firma \"web sitesi yapıyoruz\" der. Gerçek profesyonel yaklaşım şunları içerir:"
        )
    )
    body.append(
        ul(
            [
                "Teknik SEO temeli: SEO uyumlu URL yapısı, iç bağlantı mimarisi, schema markup, canonical ve hreflang kontrolü, crawl optimizasyonu. SEO sonradan eklenen bir özellik değildir; mimarinin parçasıdır.",
                "Performans mühendisliği: Core Web Vitals optimizasyonu, görsel optimizasyonu, gereksiz script azaltımı, backend sorgu iyileştirmesi. Yavaş site yalnızca sıralama değil, dönüşüm de kaybettirir.",
                "Ölçeklenebilir mimari: Çoklu dil desteği, API entegrasyonları, CRM bağlantıları, özel yazılım modülleri planlanmadan yapılan projeler kısa sürede sınırlara takılır.",
            ]
        )
    )

    body.append(h2("İstanbul'da Web Tasarım Şirketi Seçerken Nelere Dikkat Edilmeli?"))
    body.append(
        p(
            "İstanbul'daki dijital rekabet yüksektir. Bu nedenle: referans projeler, teknik yaklaşım, SEO stratejisi, süreç şeffaflığı, performans testleri dikkatle incelenmelidir. Yerel pazarı anlamayan bir yaklaşım yüzeysel kalır."
        )
    )
    body.append(
        p(
            f"Yerel hizmet detayları: {{{{ link:/tr/web-tasarim/istanbul/ }}}}."
        )
    )

    body.append(h2("Web Tasarım Firması ile Çalışma Süreci"))
    body.append(
        ul(
            [
                "Keşif ve hedef analizi",
                "Rakip araştırması",
                "Bilgi mimarisi planı",
                "UI/UX tasarım",
                "Geliştirme",
                "Test ve performans analizi",
                "Yayın ve izleme",
            ]
        )
    )
    body.append(p("Net süreç = net sonuç."))

    body.append(h2("Kurumsal Web Tasarım ve Güven"))
    body.append(
        p(
            "Kurumsal web sitesi; markanın dijital yüzüdür. Güven oluşturan unsurlar: temiz tasarım, net mesaj, hızlı yükleme, güvenli altyapı, profesyonel içerik yapısı."
        )
    )
    body.append(
        p(
            f"Kurumsal site: {{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Hazır Sistem mi, Özel Geliştirme mi?"))
    body.append(
        p(
            "Hazır sistemler hızlı başlangıç sunar. Ancak uzun vadeli SEO kontrolü ve teknik esneklik sınırlı olabilir. Özel geliştirme ise: tam kontrol, ölçeklenebilir mimari, esnek veri modeli sunabilir. Karar, hedeflere göre verilmelidir."
        )
    )
    body.append(
        p(
            f"Özel yazılım: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("En Sık Yapılan Hatalar"))
    body.append(
        ul(
            [
                "En düşük teklif üzerinden karar vermek",
                "SEO planını sormamak",
                "Performans testini incelememek",
                "İçerik stratejisini planlamamak",
            ]
        )
    )
    body.append(
        p("Web tasarım şirketi seçimi; strateji ve teknik yaklaşım temellidir.")
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Doğru web tasarım şirketi; yalnızca site üretmez, dijital altyapı kurar. SEO uyumlu, performans odaklı ve ölçeklenebilir mimari; uzun vadeli başarının temelidir."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/kurumsal-web-sitesi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/istanbul/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Profesyonel web tasarım şirketi seçiminde hedeflerinizi ve teknik beklentilerinizi paylaşın; size uygun öneriyi sunalım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Web tasarım şirketi seçerken nelere dikkat edilmeli?", "Referans projeler, teknik yaklaşım, SEO stratejisi, süreç şeffaflığı ve performans testleri değerlendirilmelidir."),
        ("Profesyonel şirket neyi farklı yapar?", "Teknik SEO temeli, performans mühendisliği ve ölçeklenebilir mimariyi baştan planlar; SEO sonradan eklenmez."),
        ("Hazır sistem mi özel geliştirme mi?", "Hedef ve ölçeklenebilirlik ihtiyacına göre; uzun vadeli kontrol için özel geliştirme daha esnektir."),
        ("İstanbul'da seçim neden daha kritik?", "Yerel rekabet yüksek; teknik hata ve yavaş site hızla sıralama ve dönüşüm kaybettirir."),
        ("En sık yapılan hatalar neler?", "Teklif odaklı karar, SEO planını sormamak, performans testini incelememek, içerik stratejisini planlamamak."),
        ("Teklif almak için ne gerekli?", "Hedef, hedef kitle, referans projeler ve teknik beklentiler yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Tasarım Şirketi | Profesyonel ve SEO Odaklı Çözümler"
    meta_description = (
        "İstanbul merkezli profesyonel web tasarım şirketi. SEO uyumlu, performans odaklı ve ölçeklenebilir web geliştirme hizmetleri."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Tasarım Şirketi — Profesyonel ve Ölçeklenebilir Çözümler",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _pricing_url(page: SeoPage) -> str:
    return f"/tr/{_service_base(page)}/fiyatlar/"


def _guide_url(page: SeoPage) -> str:
    return f"/tr/{_service_base(page)}/rehber/"


def _quote_url(page: SeoPage) -> str:
    return f"/tr/{_service_base(page)}/teklif-al/"


def _cluster_urls_for_service(page: SeoPage) -> List[str]:
    cfg = SERVICE_SILO_MAP.get(page.service.key, {}).get("tr", {})
    base = _service_base(page)
    return [f"/tr/{base}/{slug}/" for slug in cfg.get("clusters", [])]


def _topic_for_cluster_slug(service_key: str, slug: str) -> Tuple[str, List[str], List[str]]:
    """
    Returns (topic_title, pain_points, deliverables) in Turkish.
    Keep language Turkish-only; proper nouns/acronyms are allowed.
    """
    mapping = {
        # web-tasarim
        "kurumsal-web-sitesi": ("Kurumsal Web Sitesi", ["Güven ve itibar", "Hız ve erişilebilirlik", "Dönüşüm odaklı yapı"], ["Sayfa mimarisi", "Tasarım sistemi", "İçerik şablonları", "Teknik SEO temeli"]),
        "kurumsal-web-sitesi-yaptirmak": ("Kurumsal Web Sitesi Yaptırmak", ["Doğru ajans seçimi", "Kapsam belirsizliği", "Teslim sonrası bakım"], ["Kapsam dokümanı", "Zaman planı", "Bakım ve destek modeli"]),
        "istanbul": ("İstanbul’da Hizmet", ["Yerel rekabet", "Hızlı iletişim beklentisi", "Saha toplantıları"], ["Yerel odaklı teklif", "Sektör örnekleri", "İletişim planı"]),
        "ozel-yazilim-web-sitesi": ("Özel Yazılım Web Sitesi", ["Hazır altyapı sınırları", "Entegrasyon ihtiyaçları", "Ölçeklenebilirlik"], ["Özel modüller", "API entegrasyonları", "Güvenlik katmanları"]),
        "django-web-gelistirme": ("Django ile Web Geliştirme", ["Hızlı geliştirme", "Güvenlik", "Uzun vadeli sürdürülebilirlik"], ["Mimari kurulum", "Yetkilendirme", "Yönetim paneli", "Test ve yayın planı"]),
        "profesyonel-web-tasarim": ("Profesyonel Web Tasarım", ["Marka tutarlılığı", "Kullanılabilirlik", "Performans"], ["Tasarım sistemi", "Bileşen kütüphanesi", "Performans optimizasyonu"]),
        "web-tasarim-sirketi": ("Web Tasarım Şirketi", ["Süreç şeffaflığı", "İletişim", "Kalite güvencesi"], ["SLA yaklaşımı", "Sprint planı", "Dokümantasyon"]),
        "web-tasarim-freelancer": ("Freelancer ile Çalışma", ["Tek kişiye bağımlılık", "Teslim süreleri", "Bakım riski"], ["Risk azaltma kontrol listesi", "Sözleşme kalemleri"]),
        "web-developer-istanbul": ("İstanbul Web Geliştirici", ["Teknik yetkinlik doğrulama", "Referans değerlendirme"], ["Değerlendirme kriterleri", "Örnek teslim süreçleri"]),
        "ozel-yazilim-vs-hazir-site": ("Özel Yazılım mı Hazır Site mi?", ["Bütçe/kapsam dengesi", "Ölçek", "Özelleştirme"], ["Karar matrisi", "Kullanım senaryoları"]),
        "django-vs-php": ("Django ve PHP Karşılaştırması", ["Ekip yetkinliği", "Güvenlik yaklaşımı", "Geliştirme hızı"], ["Karşılaştırma tablosu", "Proje türüne göre öneri"]),
        "ajans-mi-freelancer-mi": ("Ajans mı Freelancer mı?", ["Süreklilik", "Uzmanlık çeşitliliği", "Bütçe"], ["Seçim kriterleri", "Sözleşme kontrol listesi"]),
        # mobile
        "react-native": ("React Native Uygulama", ["Tek kod tabanı", "Performans beklentisi", "Yayın süreci"], ["MVP planı", "Mağaza hazırlığı", "Analitik ve ölçümleme"]),
        "android": ("Android Uygulama", ["Cihaz çeşitliliği", "Performans", "Güvenlik"], ["Sürüm planı", "Test stratejisi"]),
        "ios": ("iOS Uygulama", ["App Store gereksinimleri", "Tasarım standartları"], ["Yayın kontrol listesi", "Sürüm notları"]),
        "ozel-mobil-uygulama": ("Özel Mobil Uygulama", ["İş hedefi uyumu", "Uzun vadeli geliştirme"], ["Ürün yol haritası", "Teknik mimari"]),
        "mobil-uygulama-nedir": ("Mobil Uygulama Nedir?", ["Doğru kullanım senaryosu", "Hedef kitle"], ["Temel kavramlar", "Örnek senaryolar"]),
        "mobil-uygulama-nasil-yapilir": ("Mobil Uygulama Nasıl Yapılır?", ["Kapsam", "Tasarımdan yayına"], ["Adım adım süreç", "Riskler ve çözümler"]),
        "mobil-uygulama-freelancer": ("Mobil Uygulama Freelancer", ["Tek kişilik ekip riski", "Süreç yönetimi"], ["Seçim kriterleri", "Teslim kontrol listesi"]),
        "react-native-vs-native": ("React Native mi Native mi?", ["Performans", "Bütçe", "Zaman"], ["Karar matrisi", "Senaryo bazlı öneri"]),
        "android-vs-ios": ("Android mi iOS mu?", ["Hedef kitle", "Bütçe", "Zaman"], ["Platform seçimi rehberi"]),
        # ecommerce
        "e-ticaret-sitesi": ("E‑Ticaret Sitesi", ["Dönüşüm oranı", "Sepet terk", "Ödeme güveni"], ["Katalog yapısı", "Ödeme entegrasyonu", "Kargo akışı"]),
        "e-ticaret-yazilimi": ("E‑Ticaret Yazılımı", ["Altyapı seçimi", "Entegrasyonlar"], ["ERP/CRM entegrasyonu", "Stok/sipariş yönetimi"]),
        "ozel-e-ticaret-yazilimi": ("Özel E‑Ticaret Yazılımı", ["Ölçek", "Özel kurallar"], ["Özel kampanya motoru", "B2B özellikleri"]),
        "b2b": ("B2B E‑Ticaret", ["Teklif listeleri", "Teklif akışı"], ["Cari hesap", "Onay akışları"]),
        "b2c": ("B2C E‑Ticaret", ["Hızlı ödeme", "Mobil deneyim"], ["Tek sayfa ödeme", "Kampanya alanları"]),
        "e-ticaret-yazilim-firmasi": ("E‑Ticaret Yazılım Firması", ["Süreç", "Destek"], ["SLA", "Bakım planı"]),
        "e-ticaret-sitesi-yaptirmak": ("E‑Ticaret Sitesi Yaptırmak", ["Kapsam", "Bütçe"], ["Planlama şablonu", "Teslim kriterleri"]),
        "e-ticaret-nedir": ("E‑Ticaret Nedir?", ["Başlangıç adımları"], ["Kavramlar", "Başlangıç kontrol listesi"]),
        "e-ticaret-sitesi-nasil-kurulur": ("E‑Ticaret Sitesi Nasıl Kurulur?", ["Doğru adımlar", "Yayın öncesi kontroller"], ["Kurulum rehberi", "Örnek yol haritası"]),
        "ozel-yazilim-vs-hazir-altyapi": ("Özel Yazılım mı Hazır Altyapı mı?", ["Bütçe", "Esneklik"], ["Karar matrisi", "Senaryolar"]),
        # seo
        "seo-danismanligi": ("SEO Danışmanlığı", ["Önceliklendirme", "Takip ve raporlama"], ["Yol haritası", "Aylık rapor"]),
        "teknik-seo": ("Teknik SEO", ["Tarama ve dizine ekleme", "Performans"], ["Logik düzeltmeler", "CWV iyileştirme"]),
        "on-page-seo": ("On‑Page SEO", ["İçerik ve yapı", "Başlık/meta"], ["Sayfa şablonları", "İç bağlantı"]),
        "seo-analizi": ("SEO Analizi", ["Sorun tespiti", "Fırsatlar"], ["Denetim raporu", "Öncelik listesi"]),
        "istanbul-seo-ajansi": ("İstanbul SEO Ajansı", ["Yerel rekabet", "Sektör odak"], ["Yerel strateji", "İçerik planı"]),
        "seo-uzmani": ("SEO Uzmanı", ["Doğru uzman seçimi"], ["Değerlendirme kriterleri"]),
        "seo-nedir": ("SEO Nedir?", ["Temel kavramlar"], ["Kısa rehber", "Örnekler"]),
        "seo-nasil-yapilir": ("SEO Nasıl Yapılır?", ["Adım adım süreç"], ["Uygulama planı"]),
        "seo-uyumlu-web-sitesi": ("SEO Uyumlu Web Sitesi", ["Mimari", "Performans"], ["Şablon standartları", "Teknik kontrol listesi"]),
        # hosting
        "hosting-hizmeti": ("Hosting Hizmeti", ["Kesintisizlik", "Güvenlik"], ["Yedekleme", "İzleme"]),
        "vps-hosting": ("VPS Hosting", ["Kaynak planlama", "Yönetim"], ["Kurulum", "Güvenlik sertleştirme"]),
        "ozel-sunucu-kiralama": ("Özel Sunucu Kiralama", ["Performans", "Bütçe"], ["Donanım seçimi", "SLA"]),
        "bulut-sunucu": ("Bulut Sunucu", ["Ölçeklenebilirlik"], ["Otomasyon", "Yedeklilik"]),
        "django-deployment": ("Django Yayınlama", ["Sürümleme", "Güvenlik"], ["CI/CD", "Nginx/WSGI ayarları"]),
        "domain-satin-al": ("Domain Satın Alma", ["Doğru alan adı", "Yönetim"], ["Kayıt ve yönlendirme"]),
        "ssl-sertifikasi": ("SSL Sertifikası", ["Güven", "Tarayıcı uyumu"], ["Kurulum", "Yenileme planı"]),
        "linux-sunucu-kurulumu": ("Linux Sunucu Kurulumu", ["Güvenlik", "Performans"], ["Kurulum adımları", "Sertleştirme"]),
        "web-hosting-fiyatlari": ("Web Hosting Planları", ["Kaynak/performans dengesi"], ["Plan karşılaştırması"]),
        "vps-fiyatlari": ("VPS Planları", ["Kaynak seçimi"], ["Örnek planlar"]),
        # ui/ux
        "ui-ux-nedir": ("UI/UX Nedir?", ["Temel kavramlar"], ["Kısa rehber", "Örnekler"]),
        "kullanici-deneyimi-tasarimi": ("Kullanıcı Deneyimi Tasarımı", ["Araştırma", "Akışlar"], ["Kullanıcı akışları", "Test planı"]),
        "kullanici-arayuzu-tasarimi": ("Kullanıcı Arayüzü Tasarımı", ["Tasarım sistemi"], ["Bileşen seti", "Stil rehberi"]),
        "ui-ux-tasarim-hizmeti": ("UI/UX Tasarım Hizmeti", ["Süreç", "Teslimatlar"], ["Figma dosyaları", "Tasarım sistemi"]),
        "mobil-uygulama-arayuz-tasarimi": ("Mobil Uygulama Arayüz Tasarımı", ["Platform kuralları"], ["Ekran seti", "Prototip"]),
        "ux-arastirmasi": ("UX Araştırması", ["Doğru içgörü"], ["Görüşmeler", "Analiz"]),
        "figma-tasarim": ("Figma Tasarım", ["Ortak çalışma"], ["Bileşen kütüphanesi"]),
        "wireframe-tasarimi": ("Wireframe Tasarımı", ["Hızlı doğrulama"], ["Akış ve iskelet"]),
        "prototype-tasarimi": ("Prototip Tasarımı", ["Test edilebilirlik"], ["Etkileşimli prototip"]),
        "ui-ux-tasarim-fiyatlari": ("UI/UX Tasarım Kapsamı", ["Kapsam", "Teslimatlar"], ["Plan yaklaşımı"]),
    }

    if slug in mapping:
        return mapping[slug]
    return (_slug_to_title(slug), ["Kapsam netliği", "Süreç yönetimi", "Kalite"], ["Planlama", "Uygulama", "Teslim kriterleri"])


def _slug_to_title(slug: str) -> str:
    parts = (slug or "").replace("-", " ").split()
    return " ".join([p.capitalize() for p in parts])


def _pick_sibling_clusters(page: SeoPage, n: int = 2) -> List[str]:
    """
    Deterministic "ring" selection to guarantee inbound links:
    each cluster links to next N clusters in the configured order.
    """
    cfg = SERVICE_SILO_MAP.get(page.service.key, {}).get("tr", {})
    slugs = list(cfg.get("clusters", []))
    if page.slug not in slugs or len(slugs) < 2:
        return []
    idx = slugs.index(page.slug)
    picks = []
    for i in range(1, n + 1):
        picks.append(slugs[(idx + i) % len(slugs)])
    base = _service_base(page)
    return [f"/tr/{base}/{s}/" for s in picks]


def _base_sections_tr(page: SeoPage, seed: str) -> List[str]:
    rnd = random.Random(seed)
    svc = _service_name(page)
    blocks: List[str] = []

    blocks.append(
        p(
            f"{svc} kapsamında karar verirken en kritik konu; hedef, kapsam ve ölçülebilir çıktıları en başta netleştirmektir. "
            f"Bu sayfa, doğru planı kurmanız ve süreç boyunca sürprizleri azaltmanız için hazırlanmıştır."
        )
    )

    blocks.append(h2("Hangi ihtiyaca hangi yaklaşım uygundur?"))
    blocks.append(
        p(
            "Başarılı projeler genellikle aynı çerçeveyi takip eder: hedef → kullanıcı → içerik/mimari → tasarım → geliştirme → test → yayın. "
            "Bu sırayı korumak, bütçe ve süre yönetimini de doğrudan kolaylaştırır."
        )
    )
    blocks.append(
        ul(
            [
                "Hedef: satış, lead, marka, operasyonel verimlilik gibi ana hedefi tek cümle ile tanımlayın.",
                "Kapsam: kritik ekranlar/sayfalar, entegrasyonlar ve yönetim ihtiyaçlarını listeleyin.",
                "Başarı ölçümü: dönüşüm, hız, kullanıcı davranışı, organik görünürlük gibi metrikleri seçin.",
            ]
        )
    )

    blocks.append(h2("Süreç ve teslimatlar"))
    blocks.append(
        p(
            "Ajans süreçlerinde şeffaflık, teslimat kalitesini artırır. Tasarım dosyaları, içerik şablonları, teknik plan ve yayın kontrol listesi "
            "gibi çıktılar; proje tamamlandıktan sonra da sürdürülebilirlik sağlar."
        )
    )
    blocks.append(
        ul(
            [
                "Bilgilendirme ve keşif: hedef ve kısıtların netleşmesi",
                "Tasarım: kullanıcı akışları, görsel dil, bileşenler",
                "Geliştirme: modüller, entegrasyonlar, performans",
                "Test ve yayın: kabul kriterleri, izleme, iyileştirme",
            ]
        )
    )

    blocks.append(h2("Kalite kontrol: sık yapılan hatalar"))
    blocks.append(
        p(
            "Kapsamın sürekli değişmesi, net olmayan sorumluluklar ve ölçülemeyen hedefler; projeyi uzatan ana etkenlerdir. "
            "Bu nedenle kabul kriterleri ve öncelikler yazılı olmalıdır."
        )
    )
    blocks.append(
        ul(
            [
                "Tek bir ‘tamamlandı’ tanımı olmadan geliştirmeye başlamak",
                "İçerik hazırlığı ve görsel ihtiyaçlarını son ana bırakmak",
                "Yayın sonrası bakım/destek planı oluşturmamak",
            ]
        )
    )

    # Soft CTA before conclusion
    blocks.append(h2("Birlikte netleştirelim"))
    blocks.append(
        cta_box(
            "Kapsamı 20 dakikada netleştirelim",
            "Hedefinizi ve mevcut durumunuzu paylaşın; en uygun yol haritasını kısa bir görüşmeyle çıkaralım.",
            _quote_url(page),
            "İletişime geçmek için teklif sayfasına gidin.",
            strong=False,
        )
    )

    blocks.append(h2("Sonuç"))
    blocks.append(
        p(
            "Doğru strateji, doğru kapsam ve iyi bir süreç yönetimi; teslim süresini kısaltır ve kaliteyi yükseltir. "
            "Bir sonraki adım, hedeflerinizi ve önceliklerinizi netleştirmektir."
        )
    )

    # Strong CTA at end
    blocks.append(
        cta_box(
            "Teklif alın",
            "Kısa bir ön görüşme ile ihtiyaçları çıkaralım ve size uygun planı sunalım.",
            _quote_url(page),
            "Teklif almak için formu açın.",
            strong=True,
        )
    )

    # Minor random extra paragraphs to reach target length naturally
    extra = [
        p(
            "Planlama aşamasında içerik mimarisini doğru kurmak, hem kullanıcı deneyimini hem de arama motoru görünürlüğünü destekler. "
            f"Bu konuda temel yaklaşımı { '{' }{ '{' } link:{_guide_url(page)} { '}' }{ '}' } üzerinden detaylıca inceleyebilirsiniz."
        ),
        p(
            "Proje boyunca ölçümleme kurmak; kararları veriye dayandırır. Basit bir raporlama yapısı bile, iyileştirme döngüsünü hızlandırır."
        ),
        p(
            "Teslim sonrası bakım, güvenlik güncellemeleri ve performans izleme; özellikle büyüyen projelerde kritik hale gelir."
        ),
    ]
    rnd.shuffle(extra)
    blocks.extend(extra)

    return blocks


def generate_tr(page: SeoPage) -> Dict:
    """
    Returns dict with:
    - title
    - meta_title
    - meta_description
    - content_html
    - faq_json
    - published_at
    """

    svc = _service_name(page)
    seed = f"tr:{page.service.key}:{page.page_type}:{page.slug}"

    if page.page_type == SeoPage.TYPE_PILLAR:
        if page.service.key == "web-design":
            return _web_design_pillar_tr(page)
        title = f"{svc}"
        meta = make_meta(
            title=title,
            meta_title=f"{svc} | Kurumsal Çözümler",
            meta_description=f"{svc} için strateji, tasarım ve geliştirme süreci. Kapsam, teslimatlar, kalite kriterleri ve teklif adımları.",
        )
        body = []
        body.append(h2("Genel bakış"))
        body.append(p(f"{svc} sayfamız, hizmet kapsamını ve çalışma yaklaşımımızı net bir çerçeveyle sunar."))
        body.extend(_base_sections_tr(page, seed))
        # Pillar should link to pricing/guide/clusters/quote via placeholders
        body.append(h2("İçerik haritası"))
        body.append(
            ul(
                [
                    f"Fiyatlandırma: {{ link:{_pricing_url(page)} }}",
                    f"Rehber: {{ link:{_guide_url(page)} }}",
                    f"Teklif: {{ link:{_quote_url(page)} }}",
                ]
            )
        )
        # add 8-12 cluster links
        cluster_urls = _cluster_urls_for_service(page)
        if cluster_urls:
            body.append(h3("Konular"))
            body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

        content_html = "\n".join(body)

        faq_json = faq(
            [
                (f"{svc} süreci nasıl ilerler?", "Keşif, planlama, tasarım, geliştirme, test ve yayın adımlarıyla ilerler; her adımda net teslimatlar belirlenir."),
                ("Teslim süresi neye göre değişir?", "Kapsam, entegrasyonlar, içerik hazırlığı ve onay hızına göre değişir. Net bir kapsam, süreyi öngörülebilir kılar."),
                ("İçerik ve görseller kim tarafından hazırlanır?", "İhtiyaca göre birlikte planlanır. Hazır içerik/görsel varsa entegrasyon yapılır; gerekirse üretim süreci ayrıca yürütülür."),
                ("Yayın sonrası destek sağlıyor musunuz?", "Evet. Bakım, izleme ve iyileştirme için aylık destek modeli kurgulanabilir."),
                ("Teklif almak için hangi bilgileri paylaşmalıyım?", "Hedef, örnek referanslar, kapsam maddeleri ve varsa teknik kısıtlar yeterlidir."),
                ("Gizlilik nasıl sağlanır?", "Gizlilik sözleşmesi ve erişim politikalarıyla proje verileri korunur."),
            ]
        )

        content_html = _ensure_word_target(page, content_html, 2000, 2500, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    if page.page_type == SeoPage.TYPE_PRICING:
        title = f"{svc} Fiyatları"
        meta = make_meta(
            title=title,
            meta_title=f"{svc} Fiyatları | Paket ve Kapsam",
            meta_description=f"{svc} fiyatları; paket yaklaşımı, kapsam belirleme ve maliyeti etkileyen kalemler. Hızlı teklif için süreci inceleyin.",
        )
        body: List[str] = []
        body.append(h2("Fiyatlandırma yaklaşımı"))
        body.append(
            p(
                "Fiyatlandırma; kapsamın netliği, entegrasyon ihtiyacı, tasarım derinliği ve teslim hızına göre şekillenir. "
                "Bu sayfa yalnızca fiyatlandırma mantığını ve bütçe planlamasını anlatır."
            )
        )
        body.append(h2("Maliyeti etkileyen ana kalemler"))
        body.append(
            ul(
                [
                    "Kapsam: sayfa/ekran sayısı, modüller, yönetim ihtiyaçları",
                    "Entegrasyonlar: ödeme, kargo, CRM/ERP, üçüncü parti servisler",
                    "Tasarım: hazır şablon uyarlama mı, özel tasarım mı",
                    "Performans ve güvenlik: optimizasyon ve sertleştirme ihtiyaçları",
                    "Bakım: yayın sonrası izleme ve iyileştirme",
                ]
            )
        )
        body.append(h2("Bütçe aralığı nasıl planlanır?"))
        body.append(
            p(
                "En sağlıklı yöntem; önce MVP (minimum uygulanabilir kapsam) tanımlamak, sonra faz faz genişletmektir. "
                "Bu sayede bütçe kontrol altında kalır ve risk azalır."
            )
        )

        # Pricing should link to quote and a few cost-related clusters if exist
        cost_clusters = [u for u in _cluster_urls_for_service(page) if any(k in u for k in ["fiyat", "maliyet"])]
        if cost_clusters:
            body.append(h3("İlgili sayfalar"))
            body.append(ul([f"{{{{ link:{u} }}}}" for u in cost_clusters[:6]]))

        body.append(h2("Hızlı teklif için gerekli bilgiler"))
        body.append(
            ul(
                [
                    "Hedef ve hedef kitle",
                    "Öncelikli modüller ve entegrasyonlar",
                    "Tasarım beklentisi (örnek siteler / referanslar)",
                    "Zaman planı ve yayın tarihi hedefi",
                ]
            )
        )
        body.append(
            cta_box(
                "Kapsamı netleştirip teklif alın",
                "Kısa bir brif ile bütçe ve takvimi hızlıca çıkaralım.",
                _quote_url(page),
                "Teklif almak için sayfaya gidin.",
                strong=True,
            )
        )
        content_html = "\n".join(body)

        faq_json = faq(
            [
                ("Fiyatlar sabit mi?", "Kapsam ve ihtiyaçlara göre değişir. Net bir kapsam dokümanı ile teklif kesinleşir."),
                ("Paket mi, özel teklif mi?", "Benzer ihtiyaçlarda paket yaklaşımı, özel ihtiyaçlarda proje bazlı teklif uygulanır."),
                ("Bakım/destek fiyatlandırmaya dahil mi?", "İhtiyaca göre ayrı kalem olarak planlanır."),
                ("Ödeme planı nasıl olur?", "Genellikle aşamalı ödeme tercih edilir: başlangıç, ara teslimler ve yayın sonrası."),
                ("Revizyonlar nasıl fiyatlandırılır?", "Kapsam içinde tanımlanan revizyonlar dahildir; kapsam dışı talepler ayrıca planlanır."),
                ("En hızlı şekilde teklif nasıl alınır?", "Hedef, kapsam maddeleri ve örnek referanslarla brif paylaşmanız yeterlidir."),
            ]
        )

        content_html = _ensure_word_target(page, content_html, 1500, 2000, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    if page.page_type == SeoPage.TYPE_GUIDE:
        title = f"{svc} Rehberi"
        meta = make_meta(
            title=title,
            meta_title=f"{svc} Rehberi | Adım Adım Süreç",
            meta_description=f"{svc} rehberi: planlama, kapsam, içerik, tasarım ve yayın adımları. Doğru kararlar için pratik kontrol listeleri.",
        )
        body: List[str] = []
        body.append(h2("Bu rehber kimler için?"))
        body.append(
            p(
                "Bu rehber; ilk kez proje başlatan ekipler, mevcut yapısını iyileştirmek isteyen markalar ve süreçlerini standardize etmek isteyen işletmeler için hazırlanmıştır."
            )
        )
        body.append(h2("1) Hedef ve kullanıcıyı netleştirin"))
        body.append(p("Başarılı bir proje; hedef, hedef kitle ve mesajın netliğiyle başlar."))
        body.append(ul(["Hedef: tek cümle", "Kullanıcı: 2–3 ana persona", "Mesaj: ana değer önerisi"]))

        body.append(h2("2) Bilgi mimarisi ve içerik planı"))
        body.append(p("Sayfa/ekran yapısı ve içerik hiyerarşisi, hem kullanıcı deneyimi hem de arama motoru görünürlüğü için belirleyicidir."))
        body.append(ul(["Ana sayfalar", "Alt konular (cluster)", "Sık sorulan sorular", "Dönüşüm noktaları"]))

        body.append(h2("3) Tasarım ve kullanılabilirlik"))
        body.append(p("Tasarım; görsellikten önce anlaşılabilirlik ve güven hissi üretmelidir."))
        body.append(ul(["Bileşen tutarlılığı", "Okunabilirlik", "Mobil öncelik", "Hız"]))

        body.append(h2("4) Geliştirme, test ve yayın"))
        body.append(p("Yayın öncesi kontrol listesi; son dakika sorunlarını azaltır."))
        body.append(ul(["Form ve dönüşüm testleri", "Hız ölçümü", "Kırık bağlantı kontrolü", "Yedekleme planı"]))

        body.append(h2("Kontrol listesi (kısa)"))
        body.append(
            ul(
                [
                    "Kapsam yazılı mı?",
                    "Teslim kriterleri net mi?",
                    "İçerikler hazır mı?",
                    "Yayın sonrası destek planı var mı?",
                ]
            )
        )

        body.append(h2("İlgili sayfalar"))
        body.append(
            ul(
                [
                    f"{{{{ link:{_pillar_url(page)} }}}}",
                    f"{{{{ link:{_pricing_url(page)} }}}}",
                    f"{{{{ link:{_quote_url(page)} }}}}",
                ]
            )
        )

        # Guide should link to 6–10 clusters (rule).
        cluster_urls = _cluster_urls_for_service(page)[:10]
        if cluster_urls:
            body.append(h3("Bu rehberle birlikte okuyun"))
            body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

        body.append(
            cta_box(
                "Kendi projenize uyarlayalım",
                "Rehberdeki adımları mevcut durumunuza göre uyarlayıp kısa bir yol haritası çıkarabiliriz.",
                _quote_url(page),
                "Teklif görüşmesi için sayfaya gidin.",
                strong=True,
            )
        )

        content_html = "\n".join(body)
        faq_json = faq(
            [
                ("Kapsam nasıl belirlenir?", "Öncelikli hedefleri belirleyip MVP tanımlayın, sonra fazlara bölün."),
                ("İçerik planı ne zaman hazırlanmalı?", "Tasarım başlamadan önce; en azından sayfa başlıkları ve temel metinler net olmalı."),
                ("Revizyon sayısı nasıl yönetilir?", "Kabul kriterleri ve revizyon kapsamı en başta yazılı olmalı."),
                ("Yayın sonrası ilk 30 günde ne yapılmalı?", "Performans izleme, kullanıcı geri bildirimi ve küçük iyileştirmeler planlanmalı."),
                ("Rehberdeki adımlar her proje için geçerli mi?", "Evet; sadece derinlik ve öncelik sırası projeye göre değişir."),
                ("Teklif almadan önce hangi bilgi yeterli?", "Hedef, kapsam maddeleri ve örnek referanslar genellikle yeterlidir."),
            ]
        )

        content_html = _ensure_word_target(page, content_html, 1800, 2200, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    if page.page_type == SeoPage.TYPE_QUOTE:
        title = f"{svc} Teklif Al"
        meta = make_meta(
            title=title,
            meta_title=f"{svc} Teklif Al | Hızlı Ön Görüşme",
            meta_description=f"{svc} için teklif almak üzere kısa bir brif paylaşın. Kapsamı netleştirip net bir plan ve zaman çizelgesi oluşturalım.",
        )
        body: List[str] = []
        body.append(h2("Teklif süreci nasıl işler?"))
        body.append(
            ul(
                [
                    "Kısa brif: hedef, kapsam ve öncelikler",
                    "Ön görüşme: soruların netleşmesi",
                    "Plan: kapsam, takvim ve teslim kriterleri",
                    "Teklif: aşamalı teslim ve ödeme planı",
                ]
            )
        )
        body.append(h2("Brifte hangi bilgileri paylaşmalısınız?"))
        body.append(
            ul(
                [
                    "İş hedefi (lead, satış, marka, verimlilik)",
                    "Öncelikli modüller ve sayfalar",
                    "Örnek beğeniler / referans siteler",
                    "Zaman planı ve kritik tarihler",
                ]
            )
        )
        body.append(h2("Güven ve şeffaflık"))
        body.append(p("Süreç boyunca net teslimatlar, anlaşılır iletişim ve yazılı kabul kriterleriyle ilerleriz."))
        body.append(
            cta_box(
                "Teklif formunu doldurun",
                "Brifinizi paylaşın; size en uygun yaklaşımı hızlıca planlayalım.",
                _quote_url(page),
                "Teklif formu için sayfayı kullanın.",
                strong=True,
            )
        )
        body.append(h2("İlgili sayfalar"))
        body.append(ul([f"{{{{ link:{_pricing_url(page)} }}}}", f"{{{{ link:{_guide_url(page)} }}}}"]))

        content_html = "\n".join(body)
        faq_json = faq(
            [
                ("Teklif ne kadar sürede hazırlanır?", "Brifin netliğine göre değişir; çoğu durumda kısa bir ön görüşmeden sonra hızla planlanır."),
                ("Görüşme online mı?", "Evet, online görüşme ile hızlıca ilerleyebiliriz."),
                ("Kapsam değişirse ne olur?", "Değişiklikler yazılı olarak değerlendirilir ve takvim/bütçe etkisi netleştirilir."),
                ("Sözleşme ve gizlilik sağlanıyor mu?", "Evet, proje başlamadan önce sözleşme ve gizlilik şartları netleştirilir."),
                ("Bakım ve destek sunuyor musunuz?", "Evet, yayın sonrası bakım ve iyileştirme için destek modeli sunulur."),
            ]
        )

        content_html = _ensure_word_target(page, content_html, 800, 1200, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    # -------------------------------------------------------------------------
    # Custom cluster: Kurumsal Web Sitesi (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "kurumsal-web-sitesi":
        return _cluster_kurumsal_web_sitesi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Kurumsal Web Sitesi Yaptırmak (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "kurumsal-web-sitesi-yaptirmak":
        return _cluster_kurumsal_web_sitesi_yaptirmak_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: İstanbul'da Hizmet (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "istanbul":
        return _cluster_istanbul_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Web Tasarım Şirketi (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-tasarim-sirketi":
        return _cluster_web_tasarim_sirketi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Ajans mı Freelancer mı? (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "ajans-mi-freelancer-mi":
        return _cluster_ajans_mi_freelancer_mi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Django ve PHP Karşılaştırması (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "django-vs-php":
        return _cluster_django_vs_php_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Django ile Web Geliştirme (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "django-web-gelistirme":
        return _cluster_django_web_gelistirme_tr(page)

    # CLUSTER
    topic_title, pain_points, deliverables = _topic_for_cluster_slug(page.service.key, page.slug)
    title = f"{topic_title}"
    meta = make_meta(
        title=title,
        meta_title=f"{topic_title} | {svc}",
        meta_description=f"{topic_title} hakkında kapsam, süreç ve teslimatlar. Doğru yaklaşımı seçmek ve hızlı teklif almak için yol haritası.",
    )
    body: List[str] = []

    body.append(h2("Kısa özet"))
    body.append(
        p(
            f"{topic_title} yaklaşımında amaç; hedefi netleştirip kapsamı doğru kurarak sürdürülebilir bir çıktı üretmektir. "
            f"Temel hizmet çerçevesi için {{ link:{_pillar_url(page)} }} sayfasını inceleyebilirsiniz."
        )
    )

    body.append(h2("En sık karşılaşılan ihtiyaçlar"))
    body.append(ul(pain_points))

    body.append(h2("Önerilen süreç"))
    body.append(
        ul(
            [
                "Keşif ve hedefler: doğru sorular, doğru kapsam",
                "Plan: teslim kriterleri ve öncelikler",
                "Uygulama: tasarım/geliştirme adımları",
                "Test ve yayın: kontrol listesi ve izleme",
            ]
        )
    )

    body.append(h2("Teslimatlar"))
    body.append(ul(deliverables))

    body.append(h2("Ne zaman bu yaklaşımı seçmelisiniz?"))
    body.append(
        p(
            "Eğer hedefleriniz ölçülebilir, kapsamınız net ve süreç yönetimine önem veriyorsanız; bu yaklaşım en iyi sonucu verir. "
            "Öncelikleri fazlara bölmek, hem bütçe hem de teslim süresi açısından avantaj sağlar."
        )
    )

    body.append(h2("İlgili sayfalar"))
    siblings = _pick_sibling_clusters(page, n=2)
    related_links = [f"{{{{ link:{_guide_url(page)} }}}}", f"{{{{ link:{_pricing_url(page)} }}}}", f"{{{{ link:{_quote_url(page)} }}}}"]
    related_links.extend([f"{{{{ link:{u} }}}}" for u in siblings])
    body.append(ul(related_links))

    body.append(
        cta_box(
            "Kapsamı netleştirip teklif alın",
            "Hedeflerinizi paylaşın; size uygun plan ve takvimi hızlıca oluşturalım.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_json = faq(
        [
            (f"{topic_title} için ilk adım nedir?", "Hedefi ve öncelikleri netleştirmek; sonra kapsamı yazılı hale getirmektir."),
            ("Teslim süresi neye bağlıdır?", "Kapsam, entegrasyonlar ve onay hızına bağlıdır."),
            ("Kapsam değişirse süreç nasıl yönetilir?", "Değişiklikler yazılı değerlendirilir; takvim ve bütçe etkisi netleştirilir."),
            ("Bu sayfa fiyat bilgisi içerir mi?", "Hayır. Fiyatlandırma yalnızca fiyat sayfasında ele alınır."),
            ("Teklif almak için ne paylaşmalıyım?", "Hedef, kapsam maddeleri, örnek beğeniler ve varsa teknik kısıtlar yeterlidir."),
        ]
    )

    content_html = _ensure_word_target(page, content_html, 1200, 1800, seed)
    return {
        "title": meta.title,
        "meta_title": meta.meta_title,
        "meta_description": meta.meta_description,
        "content_html": content_html,
        "faq_json": faq_json[:8],
        "published_at": timezone.now(),
    }


def _ensure_word_target(page: SeoPage, html: str, min_words: int, max_words: int, seed: str) -> str:
    """
    Adds non-stuffy, intent-safe paragraphs until minimum is reached.
    """
    rnd = random.Random(seed + ":pad")
    wc = word_count_from_html(html)
    if wc >= min_words:
        return html

    svc = _service_name(page)
    # Chunk bank: larger, intent-safe sections to reliably hit word targets.
    def chunk_quality() -> str:
        return "\n".join(
            [
                h2("Kalite standartları ve kabul kriterleri"),
                p(
                    "Kaliteyi artırmanın en net yolu; beklentileri ölçülebilir kabul kriterlerine dönüştürmektir. "
                    "Bu kriterler; içerik yapısı, kullanıcı akışları, performans, erişilebilirlik ve güvenlik gibi başlıklarda netleştiğinde, "
                    "proje boyunca karar almak kolaylaşır."
                ),
                p(
                    "Kabul kriterleri yalnızca son kontrolde değil; tasarım ve geliştirme sırasında da referans alınmalıdır. "
                    "Böylece revizyonlar azalır, teslim süresi daha öngörülebilir hale gelir."
                ),
                ul(
                    [
                        "Kritik sayfalar/ekranlar: hedef ve akış doğrulaması",
                        "Performans: temel hız hedefleri ve optimizasyon planı",
                        "İçerik: başlık hiyerarşisi ve şablon tutarlılığı",
                        "Güvenlik: erişim yetkileri ve temel sertleştirme",
                    ]
                ),
            ]
        )

    def chunk_process() -> str:
        return "\n".join(
            [
                h2("Süreç yönetimi: iletişim ve raporlama"),
                p(
                    "İyi bir süreç; sadece üretim değil, iletişim ve raporlama disiplinidir. "
                    "Haftalık kısa durum özeti, öncelik listesi ve bir sonraki adımların netliği; projeyi hızlandırır."
                ),
                p(
                    "Karar noktalarını yazılı hale getirmek, ekipler arası tutarlılığı artırır. "
                    "Bu yaklaşım özellikle çok paydaşlı işlerde gecikmeleri azaltır."
                ),
                ul(
                    [
                        "Haftalık özet: tamamlanan işler ve blokajlar",
                        "Öncelikler: bu hafta/gelecek hafta planı",
                        "Riskler: kapsam değişikliği, içerik gecikmesi, entegrasyon belirsizliği",
                        "Kabul: net bir ‘tamamlandı’ tanımı",
                    ]
                ),
            ]
        )

    def chunk_architecture() -> str:
        return "\n".join(
            [
                h2("Bilgi mimarisi ve iç bağlantı yaklaşımı"),
                p(
                    "Sayfa/ekran hiyerarşisi doğru kurulduğunda kullanıcılar daha hızlı doğru bilgiye ulaşır. "
                    "Aynı zamanda arama motorları, konular arasındaki ilişkiyi daha net görür. "
                    "Bu nedenle hizmet sayfası (pillar) ile alt konular (cluster) arasında planlı bir bağ kurulur."
                ),
                p(
                    f"Genel yapı için {{ link:{_pillar_url(page)} }} sayfasını; adım adım yaklaşım için {{ link:{_guide_url(page)} }} bölümünü kullanabilirsiniz."
                ),
                ul(
                    [
                        "Pillar → tüm cluster sayfaları",
                        "Guide → seçili 6–10 cluster",
                        "Cluster → pillar + ilgili sayfalar + 1–2 kardeş konu",
                        "Quote → pillar ve kapsam sayfaları",
                    ]
                ),
            ]
        )

    def chunk_scope_examples() -> str:
        return "\n".join(
            [
                h2("Kapsamı doğru tanımlamak: örnek yaklaşım"),
                p(
                    "Kapsam tanımı; sadece ‘ne yapılacak’ listesi değil, aynı zamanda ‘ne yapılmayacak’ sınırlarıdır. "
                    "Bu sınırlar net olduğunda hem bütçe hem de zaman planı daha güvenilir çıkar."
                ),
                p(
                    "Pratik bir yöntem: ihtiyaçları ‘zorunlu’, ‘öncelikli’ ve ‘isteğe bağlı’ olarak üçe ayırmak ve her madde için kabul kriteri yazmaktır. "
                    "Böylece proje ilerlerken farklı beklentiler oluşmaz."
                ),
                ul(
                    [
                        "Zorunlu: kritik akışlar ve temel sayfalar/ekranlar",
                        "Öncelikli: dönüşümü artıran iyileştirmeler",
                        "İsteğe bağlı: ikinci fazda eklenecek geliştirmeler",
                        "Kabul: her madde için ölçülebilir kontrol",
                    ]
                ),
            ]
        )

    def chunk_release() -> str:
        return "\n".join(
            [
                h2("Yayın planı ve sürdürülebilirlik"),
                p(
                    "Yayın anı, projenin bitişi değil; ölçümleme ve iyileştirme döngüsünün başlangıcıdır. "
                    "Bu nedenle yayın öncesi kontrol listesi, izleme metrikleri ve geri bildirim toplama yöntemi planlanmalıdır."
                ),
                p(
                    "Sürdürülebilirlik için; erişim yetkileri, yedekleme yaklaşımı, performans ölçümü ve düzenli bakım adımları belirlenmelidir. "
                    "Bu yaklaşım ileride oluşabilecek zorlu acil durumları azaltır."
                ),
                ul(
                    [
                        "Kontrol listesi: kritik akışlar, formlar, yönlendirmeler",
                        "İzleme: hata takibi ve temel performans metrikleri",
                        "Yedekleme: düzenli yedek ve geri dönüş planı",
                        "İyileştirme: ilk 30 günde küçük iterasyonlar",
                    ]
                ),
            ]
        )

    def chunk_pricing_only() -> str:
        return "\n".join(
            [
                h2("Fiyatlandırmada şeffaflık: teklif kalemleri"),
                p(
                    "Fiyatlandırmanın sağlıklı olması için; kapsamı üreten kalemlerin görünür olması gerekir. "
                    "Bu sayede hangi özelliklerin maliyeti artırdığı ve hangi faza taşınabileceği netleşir."
                ),
                p(
                    "En iyi uygulama; önce temel kapsamı (MVP) sabitlemek, sonra faz faz genişletmektir. "
                    "Bu yaklaşım maliyet kontrolü sağlar ve teslim süresini öngörülebilir kılar."
                ),
                ul(
                    [
                        "Kapsam: modüller, sayfa/ekran sayısı, yönetim ihtiyaçları",
                        "Entegrasyon: üçüncü parti servisler ve veri akışları",
                        "Tasarım: özel tasarım derinliği ve revizyon çerçevesi",
                        "Performans: optimizasyon ve izleme gereksinimleri",
                    ]
                ),
            ]
        )

    chunks = [chunk_quality(), chunk_process(), chunk_architecture(), chunk_scope_examples(), chunk_release()]
    if page.page_type == SeoPage.TYPE_PRICING:
        chunks.insert(0, chunk_pricing_only())

    # Add a conversion-safe chunk for non-pricing types (without stuffing)
    if page.page_type in (SeoPage.TYPE_PILLAR, SeoPage.TYPE_GUIDE, SeoPage.TYPE_CLUSTER):
        chunks.append(
            "\n".join(
                [
                    h2("Bir sonraki adım"),
                    p(
                        "Net bir yol haritası için hedefinizi ve önceliklerinizi tek sayfalık bir brif halinde paylaşmanız yeterlidir. "
                        "Kısa bir ön görüşme ile kapsamı netleştirip uygulanabilir bir plan çıkarabiliriz."
                    ),
                    p(f"Başlamak için: {{ link:{_quote_url(page)} }}"),
                ]
            )
        )

    blocks = [html]
    rnd.shuffle(chunks)
    i = 0
    while wc < min_words and i < 80:
        blocks.append(chunks[i % len(chunks)])
        wc = word_count_from_html("\n".join(blocks))
        i += 1
    return "\n".join(blocks)

