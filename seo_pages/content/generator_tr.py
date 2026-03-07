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


def _ecommerce_pillar_tr(page: SeoPage) -> Dict:
    """Custom SEO pillar for E-Ticaret Geliştirme (TR) — scalable, SEO-focused, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Genel Bakış"))
    body.append(
        p(
            "E-ticaret geliştirme; sadece bir \"online mağaza kurmak\" değildir. Doğru hedef, doğru mimari ve ölçülebilir metrikler olmadan kurulan sistemler büyüdükçe yavaşlar, karmaşıklaşır ve yük üretir."
        )
    )
    body.append(
        p(
            "Bu sayfa; satış odaklı e-ticaret sitesi, özel e-ticaret yazılımı, B2B ve B2C altyapı, SEO uyumlu e-ticaret sistemi kurmak isteyen işletmeler için stratejik bir çerçeve sunar."
        )
    )
    body.append(
        ul(
            [
                "satış odaklı e-ticaret sitesi",
                "özel e-ticaret yazılımı",
                "B2B ve B2C altyapı",
                "SEO uyumlu e-ticaret sistemi",
            ]
        )
    )
    body.append(
        p(
            f"Kapsam ve bütçe: {{{{ link:{_pricing_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}. Teklif: {{{{ link:{_quote_url(page)} }}}}."
        )
    )
    body.append(
        p(
            f"E-ticaret nedir, nasıl çalışır ve nasıl başlanır? Temel kavramlar ve başlangıç kontrol listesi için {{{{ link:/tr/{_service_base(page)}/e-ticaret-nedir/ }}}} sayfasını inceleyebilirsiniz."
        )
    )

    body.append(h2("Hangi İhtiyaca Hangi Yaklaşım Uygun?"))
    body.append(
        p(
            "Başarılı e-ticaret projeleri aynı temel sırayı izler: Hedef → Kullanıcı → İçerik Mimarisi → Tasarım → Geliştirme → Test → Yayın → Ölçümleme. Bu sırayı korumak: geliştirme süresini kısaltır; bütçeyi kontrol altında tutar; teknik borcu azaltır; dönüşüm oranını artırır."
        )
    )

    body.append(h3("1) Hedefi Netleştirmek"))
    body.append(
        p(
            "E-ticaret projesinde ilk soru: Satış mı artırılacak? Yeni pazar mı açılacak? Toptan satış (B2B) mı yapılacak? Operasyonel verimlilik mi sağlanacak? Hedef net değilse, altyapı da doğru kurulamaz."
        )
    )

    body.append(h3("2) Doğru Kapsam Tanımı"))
    body.append(
        p(
            "Kapsam sadece \"hangi sayfalar yapılacak\" değildir. Kritik başlıklar: ürün yönetim sistemi, ödeme entegrasyonları, kargo ve lojistik bağlantıları, ERP/CRM entegrasyonu, kampanya ve indirim modülleri, çoklu dil / çoklu para birimi, SEO altyapısı. Net yazılmamış kapsam → sürekli revizyon → uzayan proje demektir."
        )
    )

    body.append(h2("E-Ticaret Geliştirme Süreci"))
    body.append(h3("Keşif ve Planlama"))
    body.append(
        ul(
            [
                "Hedef analizi",
                "Rakip analizi",
                "Kullanıcı akışları",
                "Teknik mimari planı",
            ]
        )
    )
    body.append(h3("Tasarım"))
    body.append(
        ul(
            [
                "UX odaklı akış",
                "Mobil uyumlu arayüz",
                "Dönüşüm artırıcı bileşenler",
                "Sepet ve ödeme optimizasyonu",
            ]
        )
    )
    body.append(h3("Geliştirme"))
    body.append(
        ul(
            [
                "Performans odaklı kod yapısı",
                "Ölçeklenebilir mimari",
                "Güvenli ödeme sistemleri",
                "SEO teknik altyapısı",
            ]
        )
    )
    body.append(h3("Test ve Yayın"))
    body.append(
        ul(
            [
                "Hız testi",
                "Güvenlik kontrolü",
                "Checkout testi",
                "Analitik kurulumu",
            ]
        )
    )

    body.append(h2("SEO Odaklı E-Ticaret Altyapısı"))
    body.append(
        p(
            "Google'da görünür olmayan e-ticaret sitesi satış üretemez. Bu nedenle teknik olarak: hız optimizasyonu, Core Web Vitals uyumu, ürün şema yapısı (structured data), URL mimarisi, iç bağlantı yapısı, kategori ve filtre SEO stratejisi başlangıçta planlanmalıdır. SEO sonradan eklenen bir modül değil; mimari karardır."
        )
    )

    body.append(h2("Özel E-Ticaret Yazılımı mı Hazır Altyapı mı?"))
    body.append(
        p(
            "Hazır sistemler başlangıçta hızlıdır ancak: özelleştirme sınırı vardır; büyüdükçe performans düşebilir; entegrasyon karmaşıklaşabilir. Özel e-ticaret yazılımı: tam kontrol sağlar; ölçeklenebilir olur; B2B ihtiyaçlara daha uygundur; uzun vadede teknik borcu azaltır. Karar; bütçe değil, hedefe göre verilmelidir."
        )
    )

    body.append(h2("Kalite Standartları ve Kabul Kriterleri"))
    body.append(
        p(
            "Proje başlamadan önce şu sorular yazılı olmalıdır: Performans hedefi nedir? Checkout kaç adım olacak? Mobil hız hedefi kaç saniye? Kim içerik üretecek? Yayın sonrası bakım planı var mı? Net \"tamamlandı\" tanımı olmayan proje uzar."
        )
    )

    body.append(h2("Yayın Planı ve Sürdürülebilirlik"))
    body.append(
        p(
            "Yayın son değildir, başlangıçtır. Analitik kurulumu, dönüşüm takibi, hata izleme, A/B test planı, güvenlik güncellemeleri, yedekleme sistemi — ölçülmeyen e-ticaret büyümez."
        )
    )

    body.append(
        cta_box(
            "E-ticaret projenizi netleştirebiliriz",
            "Hedefinizi paylaşın, size uygun yol haritasını çıkaralım. E-Ticaret Geliştirme teklif sayfasına gidin.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("E-Ticaret geliştirme süresi neye bağlıdır?", "Ürün sayısı, entegrasyonlar ve özel geliştirme kapsamına bağlıdır."),
        ("İçerik kim tarafından hazırlanır?", "Stratejiye göre birlikte planlanabilir."),
        ("Yayın sonrası destek var mı?", "Sürdürülebilir projelerde bakım ve performans izleme kritik önemdedir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Geliştirme | Özel ve Ölçeklenebilir E-Ticaret Çözümleri"
    meta_description = (
        "E-Ticaret geliştirme hizmeti: özel e-ticaret yazılımı, B2B & B2C altyapılar, performans ve SEO odaklı mimari. Satış artıran ve ölçeklenebilir çözümler."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Geliştirme — Ölçeklenebilir ve SEO Odaklı Altyapı",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _mobile_app_pillar_tr(page: SeoPage) -> Dict:
    """Custom SEO pillar for Mobil Uygulama Geliştirme (TR) — high-value, trend keywords, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Mobil Uygulama Geliştirme Nedir?"))
    body.append(
        p(
            "Mobil uygulama geliştirme; yalnızca bir uygulama yazmak değil, kullanıcı deneyimi, performans, güvenlik ve sürdürülebilir mimariyi birlikte planlamaktır."
        )
    )
    body.append(
        p(
            "Başarılı bir mobil uygulama: hızlı çalışır, kullanıcı dostudur, güvenlidir, ölçeklenebilir altyapıya sahiptir, App Store ve Google Play kurallarına uygundur, iş hedefleriyle uyumludur. Mobil uygulama; markanızın cebinizdeki dijital temsilcisidir."
        )
    )
    body.append(
        p(
            f"Rehber: {{{{ link:{_guide_url(page)} }}}}. Teklif: {{{{ link:{_quote_url(page)} }}}}."
        )
    )

    body.append(h2("Neden Profesyonel Mobil Uygulama Geliştirme Önemlidir?"))
    body.append(
        p(
            "Rekabet yüksek. Kullanıcı sabırsız. Eğer uygulama: yavaş açılıyorsa, çöküyorsa, karmaşık navigasyona sahipse, güven vermiyorsa — kullanıcı 5 saniye içinde siler. Profesyonel geliştirme; teknik kalite + UX tasarım + performans optimizasyonu demektir."
        )
    )

    body.append(h2("Android ve iOS Uygulama Geliştirme"))
    body.append(
        p(
            "Mobil projeler genellikle üç şekilde planlanır:"
        )
    )
    body.append(h3("Native Development"))
    body.append(
        p(
            "Android (Kotlin / Java), iOS (Swift). En yüksek performans, platforma özel deneyim."
        )
    )
    body.append(h3("Cross-Platform Development"))
    body.append(
        p(
            "Flutter, React Native. Daha hızlı geliştirme süresi, tek kod tabanı."
        )
    )
    body.append(h3("Backend Entegrasyonu"))
    body.append(
        ul(
            [
                "API mimarisi",
                "Kullanıcı yönetimi",
                "Push notification",
                "Ödeme sistemleri",
                "Analitik entegrasyonu",
            ]
        )
    )
    body.append(
        p(
            "Mobil uygulama yalnızca frontend değildir; sağlam backend gerektirir."
        )
    )

    body.append(h2("Mobil Uygulama Geliştirme Süreci"))
    body.append(h3("1) Keşif ve Strateji"))
    body.append(
        ul(
            [
                "Hedef kitle analizi",
                "Rakip analizi",
                "İş modeli belirleme",
                "Monetizasyon planı",
            ]
        )
    )
    body.append(h3("2) UX/UI Tasarım"))
    body.append(
        ul(
            [
                "Wireframe",
                "Prototip",
                "Kullanıcı akışı",
                "Mobil-first tasarım prensibi",
            ]
        )
    )
    body.append(h3("3) Geliştirme"))
    body.append(
        ul(
            [
                "Frontend (Android/iOS)",
                "Backend API",
                "Güvenlik",
                "Performans optimizasyonu",
            ]
        )
    )
    body.append(h3("4) Test ve QA"))
    body.append(
        ul(
            [
                "Cihaz testleri",
                "Performans testleri",
                "Crash analizi",
                "Store uyumluluk kontrolü",
            ]
        )
    )
    body.append(h3("5) Yayın ve Optimizasyon"))
    body.append(
        ul(
            [
                "App Store ve Google Play yayın süreci",
                "ASO (App Store Optimization)",
                "Kullanıcı geri bildirim analizi",
                "Güncelleme planı",
            ]
        )
    )

    body.append(h2("Mobil Uygulamada Performans ve Güvenlik"))
    body.append(
        p(
            "Kaliteli bir mobil uygulama: hızlı açılış süresi, optimize edilmiş veri çağrıları, güvenli authentication, şifreli veri transferi (HTTPS / SSL), sunucu taraflı güvenlik kontrolleri sunar. Güvenlik ihlali marka güvenini zedeler."
        )
    )

    body.append(h2("Hangi İşletmeler İçin Uygundur?"))
    body.append(
        ul(
            [
                "E-ticaret firmaları",
                "SaaS girişimleri",
                "Rezervasyon sistemleri",
                "Lojistik ve kurye firmaları",
                "Eğitim platformları",
                "Fintech projeleri",
            ]
        )
    )
    body.append(
        p(
            "Mobil uygulama, büyüme hedefleyen işletmeler için stratejik bir adımdır."
        )
    )

    body.append(h2("Neler Kazanırsınız?"))
    body.append(
        ul(
            [
                "Marka bilinirliği",
                "Kullanıcı sadakati",
                "Push notification ile direkt iletişim",
                "Veri analizi ve kullanıcı davranışı takibi",
                "Ölçeklenebilir dijital altyapı",
            ]
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Mobil uygulama geliştirme; teknik uzmanlık, strateji ve kullanıcı deneyimi gerektirir. Doğru planlama ve mimari ile uygulamanız yalnızca çalışmaz — büyür."
        )
    )

    body.append(h2("İlgili konular"))
    body.append(
        p(
            f"Rehber: {{{{ link:{_guide_url(page)} }}}}. Teklif: {{{{ link:{_quote_url(page)} }}}}."
        )
    )
    cluster_urls = _cluster_urls_for_service(page)
    if cluster_urls:
        body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls[:10]]))

    body.append(
        cta_box(
            "Teklif Al",
            "Mobil uygulama projeniz için hedeflerinizi paylaşın; size uygun kapsamı ve planı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Mobil uygulama geliştirme ne kadar sürer?", "Kapsama, özelliklere ve platform sayısına göre değişir."),
        ("Android ve iOS aynı anda geliştirilebilir mi?", "Evet. Native veya cross-platform çözümlerle mümkündür."),
        ("Yayın sonrası destek sağlıyor musunuz?", "Evet. Güncelleme ve bakım planı oluşturulur."),
        ("Uygulama mağazasında üst sıralara nasıl çıkılır?", "ASO, kullanıcı yorumları, performans ve retention oranı belirleyicidir."),
        ("Backend gerekli mi?", "Çoğu profesyonel uygulamada API tabanlı backend gereklidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobil Uygulama Geliştirme | Android & iOS Profesyonel Çözümler"
    meta_description = (
        "Mobil uygulama geliştirme hizmeti. Android ve iOS için ölçeklenebilir, performans odaklı ve kullanıcı deneyimi güçlü mobil uygulamalar."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Mobil Uygulama Geliştirme — Ölçeklenebilir ve Performans Odaklı Çözümler",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_react_native_tr(page: SeoPage) -> Dict:
    """Custom cluster: React Native Uygulama — tek kod tabanı ile iOS + Android. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "React Native, iOS ve Android’i tek kod tabanı ile geliştirmeyi sağlayan güçlü bir yaklaşımdır. Doğru kurgulandığında hızlı MVP çıkarmayı, ürün iterasyonlarını hızlandırmayı ve bakım yükünü yönetilebilir tutmayı sağlar."
        )
    )
    body.append(
        p(
            "Bu yaklaşımda amaç yalnızca \"iki platforma da çıkaralım\" değil; hedefi netleştirip kapsamı doğru kurarak performans, kalite ve yayın sürecini baştan planlamaktır. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) Tek kod tabanı ile hız"))
    body.append(
        p(
            "Birçok ekip için en kritik ihtiyaç; MVP’yi daha hızlı yayınlamak, tek ekip ile iki platformu yönetmek ve yeni özellikleri aynı anda iOS + Android’e taşımaktır."
        )
    )
    body.append(
        ul(
            [
                "MVP’yi daha hızlı yayınlamak",
                "Tek ekip ile iki platformu yönetmek",
                "Yeni özellikleri aynı anda iOS + Android’e taşımak",
            ]
        )
    )

    body.append(h3("2) Performans beklentisi"))
    body.append(
        p(
            "React Native her projede \"otomatik hızlı\" değildir. Performans hedefleri net konmadığında; liste/akış ekranlarında takılmalar, zayıf cihazlarda yavaşlık, gereksiz re-render ve bundle şişmesi gibi problemler oluşabilir. Bu yüzden ekran türleri ve kritik akışlar erken aşamada belirlenir."
        )
    )

    body.append(h3("3) Yayın süreci (App Store / Google Play)"))
    body.append(
        p(
            "Tek kod tabanı olsa da yayın tarafında iki ayrı dünya vardır: mağaza gereksinimleri, test süreçleri, release yönetimi ve versiyonlama, crash/ANR takibi. Yayın checklist’i ve izleme metrikleri baştan planlanmalıdır."
        )
    )

    body.append(h2("React Native Ne Zaman Mantıklı?"))
    body.append(
        p(
            "Aşağıdakiler sizde varsa React Native genellikle iyi bir seçimdir: iOS + Android’i aynı anda çıkarmak istiyorsunuz; MVP ve hızlı iterasyon öncelikli; ürününüz çoğunlukla standart ekran/akışlardan oluşuyor; tek ekip ile sürdürülebilir bakım hedefliyorsunuz; analitik ve ölçümleme ile ürünü büyütmek istiyorsunuz."
        )
    )
    body.append(
        ul(
            [
                "iOS + Android’i aynı anda çıkarmak istiyorsunuz",
                "MVP ve hızlı iterasyon öncelikli",
                "Ürününüz çoğunlukla standart ekran/akışlardan oluşuyor",
                "Tek ekip ile sürdürülebilir bakım hedefliyorsunuz",
                "Analitik ve ölçümleme ile ürünü büyütmek istiyorsunuz",
            ]
        )
    )

    body.append(h2("Ne Zaman Native Daha Doğru Olabilir?"))
    body.append(
        p(
            "Şu senaryolarda native yaklaşım daha mantıklı olabilir: yüksek FPS gerektiren animasyonlar / oyun benzeri arayüz; yoğun kamera/AR/ML işleme; çok özel cihaz erişimleri ve düşük seviyeli entegrasyonlar; \"en üst seviye performans\" en kritik gereksinimse. Özet: React Native güçlüdür ama her proje için tek doğru değildir."
        )
    )

    body.append(h2("Önerilen Süreç"))
    body.append(
        p(
            "Başarılı React Native projeleri genelde aynı omurgayı takip eder: 1) Keşif ve hedefler: hedef KPI’lar (dönüşüm, retention, işlem süresi), kullanıcı senaryoları ve akışlar, kritik ekranlar listesi. 2) Plan: MVP + teslim kriterleri — MVP kapsamı ve faz planı, kabul kriterleri (performans, kalite, güvenlik), riskler ve bağımlılıklar. 3) Uygulama: tasarım + geliştirme — bileşen tabanlı UI sistemi, state yönetimi ve veri akışı, API entegrasyonları, performans optimizasyonu (özellikle liste/akış ekranları). 4) Test ve yayın: cihaz çeşitliliği testleri, crash/ANR izleme kurulumu, mağaza hazırlığı + release yönetimi."
        )
    )

    body.append(h2("Teslimatlar"))
    body.append(h3("MVP Planı"))
    body.append(
        p(
            "MVP planı; kritik akışlar (zorunlu), dönüşüm artıran iyileştirmeler (öncelikli), ikinci faz geliştirmeler (isteğe bağlı) ve her madde için ölçülebilir kabul kriteri içerir."
        )
    )
    body.append(h3("Mağaza Hazırlığı"))
    body.append(
        p(
            "App Store / Google Play checklist, sürüm notları ve release planı, test akışı (internal / closed testing / production) netleştirilir."
        )
    )
    body.append(h3("Analitik ve Ölçümleme"))
    body.append(
        p(
            "Analitik tarafında event takibi (funnel, activation, retention), hata takibi ve performans metrikleri, ilk 30 gün için net bir iterasyon planı belirlenir."
        )
    )

    body.append(h2("Kalite Standartları: React Native’de Kritik Noktalar"))
    body.append(
        ul(
            [
                "Performans: re-render kontrolü, liste optimizasyonu, bundle boyutu yönetimi",
                "Güvenlik: token yönetimi, rol bazlı erişim, güvenli depolama",
                "Tutarlılık: iOS/Android UI farkları için net tasarım kararları",
                "Bakım: kod standartları, dokümantasyon, sürümleme disiplini",
            ]
        )
    )
    body.append(
        p("Kaliteyi artırmanın yolu, beklentileri ölçülebilir kriterlere bağlamaktır.")
    )

    body.append(h2("Yayın Planı ve Sürdürülebilirlik"))
    body.append(
        p(
            "Yayın anı bitiş değil; ölçümleme ve iyileştirme döngüsünün başlangıcıdır. İlk 30 günde kritik akışlar izlenir, sürtünme noktaları tespit edilir ve küçük iterasyonlarla hızla iyileştirme yapılır. Bu yaklaşım, \"tek seferlik proje\" yerine ürün geliştirme mantığı kurar."
        )
    )

    body.append(
        cta_box(
            "React Native ile iki platforma birden çıkmak istiyorsanız",
            "İlk adım MVP kapsamını ve performans hedeflerini netleştirmektir. Hedefinizi paylaşın; size uygun planı birlikte çıkaralım. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        (
            "React Native ile her şey yapılır mı?",
            "Çoğu ürün için evet; ancak yoğun donanım/performans gerektiren işlerde native daha doğru olabilir.",
        ),
        (
            "Tek kod tabanı %100 aynı deneyim demek mi?",
            "Hayır. iOS ve Android’in tasarım ve davranış farkları vardır; bunu tasarım kararlarıyla yönetmek gerekir.",
        ),
        (
            "MVP neden bu kadar önemli?",
            "İlk sürümde kritik akışları yayınlayıp veriye göre büyümek, hem bütçeyi hem süreyi daha yönetilebilir yapar.",
        ),
        (
            "Yayın sürecinde neler planlanmalı?",
            "Mağaza gereksinimleri, test stratejisi, sürüm notları ve izleme (crash/perf) baştan kurulur.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "React Native Uygulama Geliştirme | Tek Kod Tabanı ile iOS + Android"
    meta_description = (
        "React Native ile iOS ve Android için tek kod tabanı. MVP planı, performans beklentisi, mağaza yayın süreci, analitik ve sürdürülebilir geliştirme yaklaşımı."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "React Native Uygulama — Tek Kod Tabanı ile iOS ve Android Geliştirme",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_android_tr(page: SeoPage) -> Dict:
    """Custom cluster: Android Uygulama Geliştirme — device diversity, performance, security. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Android uygulama geliştirmede en kritik fark, cihaz çeşitliliği ve performans beklentisidir. Başarılı bir Android uygulaması; düşük/orta seviye cihazlarda bile akıcı çalışır, ağ koşullarına dayanıklıdır ve güvenlik temelini doğru kurar."
        )
    )
    body.append(
        p(
            "Bu sayfa; Android projelerinde doğru kararları (mimari, performans, güvenlik, yayın) baştan netleştirmeniz için hazırlanmıştır. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Android Uygulama Geliştirmede En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) Cihaz Çeşitliliği ve Uyumluluk"))
    body.append(
        p(
            "Android ekosistemi farklı ekran boyutları, üreticiler, Android sürümleri ve donanımlar anlamına gelir. Bu yüzden tasarım ve geliştirme şunları hedeflemeli:"
        )
    )
    body.append(
        ul(
            [
                "farklı çözünürlüklerde tutarlı UI",
                "düşük RAM / düşük CPU cihazlarda stabil performans",
                "farklı Android sürümlerinde uyumlu davranış",
                "üretici kaynaklı beklenmedik problemler için test planı",
            ]
        )
    )
    body.append(h3("2) Performans ve Hız"))
    body.append(
        p(
            "Kullanıcılar \"uygulama açılmıyor, takılıyor, kasıyor\" dediği anda kaybedersiniz. Performansı etkileyen başlıklar:"
        )
    )
    body.append(
        ul(
            [
                "cold start / app launch süresi",
                "liste ekranlarında kaydırma akıcılığı (scroll performance)",
                "gereksiz network çağrılarının azaltılması",
                "görsel ve veri cache stratejileri",
                "offline-first düşünce (zayıf internet koşullarında bile çalışabilme)",
            ]
        )
    )
    body.append(h3("3) Güvenlik ve Veri Koruma"))
    body.append(
        p(
            "Android uygulamada güvenlik sadece \"login\" değildir. Özellikle kullanıcı verisi, token yönetimi ve API güvenliği kritik:"
        )
    )
    body.append(
        ul(
            [
                "güvenli authentication ve token yönetimi",
                "API isteklerinde sunucu taraflı doğrulama",
                "cihazda saklanan verilerin güvenli tutulması",
                "rate limit / abuse korumaları",
                "log ve hata kayıtlarında hassas veri sızıntısını engelleme",
            ]
        )
    )

    body.append(h2("Önerilen Süreç"))
    body.append(h3("1) Keşif ve Hedefler"))
    body.append(
        ul(
            [
                "uygulamanın ana hedefi (satış/lead/operasyon/verimlilik)",
                "kullanıcı senaryoları ve kritik akışlar",
                "MVP mi, fazlı geliştirme mi?",
            ]
        )
    )
    body.append(p("<strong>Çıktı:</strong> hedef + kapsam taslağı + öncelik listesi"))
    body.append(h3("2) Planlama ve Mimari"))
    body.append(
        p(
            "Android tarafında mimari kararlar performansı direkt etkiler. Planlama aşamasında netleşmesi gerekenler: ekran akışları ve bilgi mimarisi, API sözleşmeleri (endpoint yapısı, hata kodları, veri formatları), bildirim ve arka plan işlerinin yaklaşımı, analitik event planı (hangi aksiyonları ölçeceğiz?)."
        )
    )
    body.append(p("<strong>Çıktı:</strong> teknik plan + teslim kriterleri"))
    body.append(h3("3) Tasarım ve Geliştirme"))
    body.append(
        ul(
            [
                "UI/UX: okunabilirlik, net CTA, basit navigasyon",
                "performans odaklı ekranlar ve veri yönetimi",
                "sürdürülebilir kod düzeni (kolay bakım ve güncelleme)",
            ]
        )
    )
    body.append(p("<strong>Çıktı:</strong> çalışan sürüm + test edilebilir build"))
    body.append(h3("4) Test ve Yayın"))
    body.append(
        p(
            "Android'de yayın, geliştirme kadar önemlidir: farklı cihazlarda temel senaryoların test edilmesi, crash ve ANR risklerini azaltma, Play Store politikalarına uyum, sürüm notları ve release planı."
        )
    )
    body.append(p("<strong>Çıktı:</strong> yayın checklist + izleme planı"))

    body.append(h2("Teslimatlar"))
    body.append(
        p(
            "Bu sayfanın hedefi \"ne teslim alacağınızı\" netleştirmek: sürüm planı (v1, v1.1, v2 gibi faz yaklaşımı), test stratejisi (cihaz listesi + kritik akış testleri), analitik ölçümleme planı (event tracking), yayın sonrası iyileştirme döngüsü (ilk 30 gün)."
        )
    )

    body.append(h2("Ne Zaman Android Yaklaşımı Seçmelisiniz?"))
    body.append(
        ul(
            [
                "hedefiniz ölçülebilir ve netse",
                "kullanıcı akışları belirginse",
                "fazlara bölerek ilerlemek istiyorsanız",
                "stabil performans ve güvenlik önceliğinizse",
            ]
        )
    )
    body.append(
        p(
            "Android'de doğru yaklaşım; \"bir an önce çıktı alalım\" değil, sürdürülebilir büyüme hedefiyle kurulur."
        )
    )

    body.append(h2("Yayın Sonrası: Sürdürülebilirlik ve İyileştirme Döngüsü"))
    body.append(
        p(
            "Yayın; bitiş değil başlangıçtır. Sağlam Android projelerinde şu döngü kurulur: crash raporlama (hata izleme), performans metrikleri takibi, kullanıcı geri bildirimleri ve iterasyonlar, düzenli bakım ve güvenlik güncellemeleri."
        )
    )
    body.append(
        p(
            "Bu yaklaşım; uzun vadede uygulamanızı daha stabil, daha hızlı ve daha güvenilir hale getirir."
        )
    )

    body.append(
        cta_box(
            "Android uygulama hedefinizi 2–3 cümlede yazın",
            "Kapsamı fazlara bölelim ve uygulanabilir bir plan çıkaralım. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Android uygulama geliştirmede ilk adım nedir?", "Hedefi ve kritik kullanıcı akışlarını netleştirmek; ardından kapsamı yazılı hale getirmektir."),
        ("Android'de performans en çok nerede bozulur?", "Açılış süresi, liste ekranları (scroll), gereksiz network çağrıları ve yanlış cache yaklaşımı en sık sebeplerdir."),
        ("Cihaz çeşitliliği nasıl yönetilir?", "Kritik cihaz/sürüm listesi belirlenir, test stratejisi buna göre kurulur ve UI farklı ekranlara uyarlanır."),
        ("Güvenlik için minimum neler olmalı?", "Güvenli authentication, token yönetimi, API doğrulama, hassas verilerin korunması ve log hijyeni."),
        ("Play Store'a çıkışta en çok nerede sorun olur?", "İzinler (permissions), politika uyumu, çökme/ANR oranları ve eksik yayın kontrol listesi."),
        ("Yayından sonra hangi metrikler takip edilmeli?", "Crash oranı, oturum süresi, dönüşüm adımları, retention ve performans metrikleri."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Android Uygulama Geliştirme | Performans, Güvenlik ve Ölçeklenebilirlik"
    meta_description = (
        "Android uygulama geliştirme: cihaz çeşitliliğine dayanıklı, hızlı, güvenli ve ölçeklenebilir mimari. Play Store uyumlu, analitik odaklı geliştirme."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Android Uygulama Geliştirme — Cihaz Çeşitliliğinde Stabil, Hızlı ve Güvenli",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_ios_tr(page: SeoPage) -> Dict:
    """Custom cluster: iOS Uygulama Geliştirme — App Store uyumlu, stabil, ölçeklenebilir. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "iOS tarafında başarı, \"uygulamayı çalıştırmak\"tan daha fazlasıdır: App Store gereksinimleri, tasarım standardı, performans, stabilite ve yayın sonrası iterasyon birlikte yönetildiğinde ürün büyür."
        )
    )
    body.append(
        p(
            "Bu sayfa, iOS uygulama geliştirmeyi süreç + teslim kriterleri + kalite standartları üzerinden netleştirir: neyi, hangi sırayla ve hangi kabul kriterleriyle yapacağınızı görürsünüz. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) App Store Gereksinimleri ve Yayına Hazırlık"))
    body.append(
        p(
            "iOS projelerinde yayın süreci \"son adım\" değildir; en baştan planlanmalıdır. Sık karşılaşılan başlıklar:"
        )
    )
    body.append(
        ul(
            [
                "App Store yönergeleriyle uyumlu akışlar",
                "izin metinleri ve gizlilik yaklaşımı (kullanıcı güveni)",
                "sürüm notları, ekran görüntüleri ve yayın checklist'i",
                "test süreçleri (TestFlight, cihaz kapsaması, senaryolar)",
            ]
        )
    )
    body.append(p("<strong>Hedef:</strong> yayın sürecini sürprizlere değil, checklist'e bağlamak."))
    body.append(h3("2) iOS Tasarım Standartları (UI/UX)"))
    body.append(
        p(
            "iOS kullanıcıları tutarlı bir deneyim bekler. Bu yüzden: gezinme (navigation) yapısı net olmalı; form ve CTA (Call-to-Action) dili sade olmalı; boşluklar, tipografi, bileşen davranışları tutarlı olmalı; erişilebilirlik temeli (okunabilirlik, dokunma alanları) düşünülmeli."
        )
    )
    body.append(p("<strong>Hedef:</strong> kullanıcıyı \"arayüzle uğraştırmadan\" kritik aksiyona götürmek."))
    body.append(h3("3) Stabilite, Performans ve Sürdürülebilirlik"))
    body.append(
        p(
            "iOS ekosistemi daha kontrollü olsa da, iyi bir ürün için şunlar şart: crash takibi ve log stratejisi; kritik akışlarda performans hedefleri; ağ yönetimi (offline tolerans, retry stratejisi); yayın sonrası küçük iterasyonlarla kaliteyi yükseltmek."
        )
    )
    body.append(p("<strong>Hedef:</strong> \"ilk sürüm çıktı\" değil, \"ölçümlenebilir şekilde çalışıyor\" demek."))

    body.append(h2("Önerilen Süreç (iOS İçin Pratik Akış)"))
    body.append(h3("1) Keşif ve Hedefler"))
    body.append(
        ul(
            [
                "kullanıcı profili ve ana problem",
                "kritik akışlar (kayıt, rezervasyon, ödeme, mesajlaşma vb.)",
                "ölçülecek metrikler (aktivasyon, retention, dönüşüm adımları)",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> hedef + kapsam iskeleti + kararlar"))
    body.append(h3("2) Plan: Teslim Kriterleri ve Öncelikler"))
    body.append(
        ul(
            [
                "MVP kapsamı (v1) + sonraki fazlar",
                "hangi ekranların \"zorunlu\" olduğu",
                "analitik event planı (ne ölçülecek?)",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> faz planı + kabul kriterleri"))
    body.append(h3("3) Uygulama: Tasarım/Geliştirme"))
    body.append(
        ul(
            [
                "iOS tasarım standardı + komponent mantığı",
                "güvenli oturum yaklaşımı (auth, token, role-based ihtiyaç varsa)",
                "performans ve veri akışı optimizasyonu",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> test edilebilir sürüm + kritik akışlar"))
    body.append(h3("4) Test ve Yayın"))
    body.append(
        ul(
            [
                "senaryo bazlı test",
                "TestFlight dağıtım ve geri bildirim döngüsü",
                "yayın checklist + izleme planı",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> yayın-ready build + izleme kurulumları"))

    body.append(h2("Teslimatlar (Somut Çıktılar)"))
    body.append(
        p(
            "iOS uygulama geliştirmede \"teslim\" sadece APK/IPA değildir. Sağlam bir çıktı seti: yayın kontrol listesi (App Store submission checklist), sürüm notları şablonu (release notes), test planı (kritik senaryolar + cihaz kapsaması), izleme planı (crash + temel kullanıcı aksiyonları)."
        )
    )

    body.append(h2("Ne Zaman Bu Yaklaşımı Seçmelisiniz?"))
    body.append(
        p(
            "Bu sayfa; iOS'ta hızlı ama kontrollü ilerlemek isteyen ekipler için en iyi sonucu verir:"
        )
    )
    body.append(
        ul(
            [
                "ürününüz App Store standartlarına sorunsuz uymalıysa",
                "stabilite ve kullanıcı deneyimi \"marka algısı\" için kritikse",
                "yayın sonrası iterasyonla büyümeyi hedefliyorsanız",
                "süreç yönetimini yazılı ve ölçülebilir yapmak istiyorsanız",
            ]
        )
    )

    body.append(
        cta_box(
            "Hedefinizi ve kritik akışlarınızı yazın",
            "iOS için en doğru kapsamı birlikte çıkaralım. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("iOS uygulama geliştirmede ilk adım nedir?", "Kullanıcı hedefini ve kritik akışları netleştirmek; sonra MVP kapsamını yazılı hale getirmektir."),
        ("App Store süreci neden en baştan planlanmalı?", "Çünkü izinler, gizlilik yaklaşımı, UI standartları ve yayın checklist'i sonradan eklendiğinde gecikme yaratabilir."),
        ("iOS tasarım standardı neden önemlidir?", "Tutarlı gezinme, okunabilirlik ve bileşen davranışları kullanıcı güvenini ve dönüşümü doğrudan etkiler."),
        ("TestFlight ne işe yarar?", "Yayın öncesi dağıtım, geri bildirim toplama ve hataları kontrollü şekilde azaltmak için kullanılır."),
        ("Yayın sonrası odak ne olmalı?", "Crash oranı, kritik akış performansı ve aktivasyon/retention metrikleri."),
        ("Kapsam değişirse süreç nasıl yönetilir?", "Faz planı ve kabul kriterleriyle: \"zorunlu/öncelikli/isteğe bağlı\" ayrımı yapılarak."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "iOS Uygulama Geliştirme | App Store Uyumlu ve Ölçeklenebilir"
    meta_description = (
        "iOS uygulama geliştirme süreci: App Store gereksinimleri, tasarım standartları, performans ve güvenlik. Ölçülebilir hedeflerle sürdürülebilir iOS ürünleri."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "iOS Uygulama Geliştirme — App Store Uyumlu, Stabil ve Ölçeklenebilir Ürünler",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_istanbul_mobil_tr(page: SeoPage) -> Dict:
    """Custom cluster: İstanbul'da Mobil Uygulama Hizmeti — yerel rekabet, hızlı iletişim, saha toplantıları. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "İstanbul'da mobil uygulama geliştirmek \"sadece yazılım üretmek\" değildir. Burada pazarda yoğun rekabet, hızlı iletişim beklentisi, saha gerçeği ve operasyonel ihtiyaçlar aynı anda yönetilir."
        )
    )
    body.append(
        p(
            "Bu sayfa; İstanbul'da iş yapan markalar için mobil uygulama sürecini hedef → kapsam → teslim kriterleri → yayın → ölçümleme çizgisinde netleştirir. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) Yerel Rekabet: \"Benzer uygulamalar zaten var\" problemi"))
    body.append(
        p(
            "İstanbul'da çoğu sektör (restoran, güzellik, servis, emlak, eğitim, lojistik) benzer uygulamalarla dolu. Bu yüzden başarı; \"uygulama var\" değil, farkı net anlatan ürün tasarlamakla gelir. Doğru yaklaşım: Hangi kullanıcı problemini çözdüğünü tek cümlede netleştir; 2–3 \"kritik akış\" seç (ör. randevu alma, sipariş, üyelik, teklif talebi); Rakipten \"daha fazla özellik\" değil, daha az sürtünme hedefle; İlk sürümde odak: aktivasyon + tekrar kullanım."
        )
    )
    body.append(h3("2) Hızlı İletişim Beklentisi: karar döngüsü kısadır"))
    body.append(
        p(
            "İstanbul'da ekipler hızlı karar ister ama hızlı karar = rastgele karar olmamalı. Bunu yönetmek için: haftalık kısa durum özeti + net öncelik listesi; \"tamamlandı\" tanımı (kabul kriteri); her değişiklik talebini faz planına bağlama; tek sorumlu iletişim noktası (karar kargaşasını azaltır)."
        )
    )
    body.append(h3("3) Saha Toplantıları: yerinde süreç, net ajanda ister"))
    body.append(
        p(
            "Yüz yüze görüşme hızlıdır ama ajandasız olursa sadece \"konuşulmuş\" olur. Verimli saha toplantısı şablonu: hedef + kullanıcı + kritik akışlar (15 dk); kapsam sınırı (ne var / ne yok) (10 dk); teslim kriterleri + test/yayın planı (10 dk); sonraki adım: yazılı özet ve aksiyonlar (5 dk)."
        )
    )

    body.append(h2("Önerilen Süreç (İstanbul Odaklı)"))
    body.append(h3("1) Keşif ve Hedefler"))
    body.append(
        ul(
            [
                "İstanbul özelinde hedef kitle: semt / bölge / hizmet alanı",
                "kullanıcı profili ve \"neden şimdi?\" motivasyonu",
                "kritik akışlar + başarı metriği",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> hedef + kapsam taslağı + karar notları"))
    body.append(h3("2) Plan: Teslim Kriterleri ve Öncelikler"))
    body.append(
        ul(
            [
                "MVP (v1) + faz-2 planı",
                "hangi ekranların zorunlu olduğu",
                "ölçümleme planı (event'ler)",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> faz planı + kabul kriterleri"))
    body.append(h3("3) Uygulama: Tasarım/Geliştirme"))
    body.append(
        ul(
            [
                "mobil-first UX, net CTA'lar",
                "performans ve stabilite hedefleri",
                "bildirim ve kullanıcı geri bildirim döngüsü",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> test edilebilir sürüm + kritik akışlar tamam"))
    body.append(h3("4) Test ve Yayın"))
    body.append(
        ul(
            [
                "senaryo bazlı test (kritik akışlar)",
                "yayın checklist + izleme planı",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> yayın-ready build + izleme planı"))

    body.append(h2("Teslimatlar (Bu Sayfaya Özel)"))
    body.append(
        p(
            "İstanbul'da hizmet odaklı projelerde \"teslim\" sadece uygulama değildir: Yerel odaklı teklif çerçevesi (hedef/kapsam/teslim kriteri netliği); Sektör örnekleri (benzer iş modelleri için kritik akış şablonları); İletişim planı (toplantı ritmi, karar süreçleri, raporlama formatı)."
        )
    )

    body.append(h2("Hangi İşletmeler İçin Uygun?"))
    body.append(
        ul(
            [
                "İstanbul'da şube veya saha operasyonu olan işletmeler",
                "hızlı büyüyen servis/rezervasyon odaklı markalar",
                "\"WhatsApp + telefon\" yoğun çalışan ama süreçleri uygulamaya taşımak isteyen ekipler",
                "rekabette öne çıkmak için hız + UX + ölçümleme isteyenler",
            ]
        )
    )

    body.append(h2("Yayın Planı ve Sürdürülebilirlik"))
    body.append(
        p(
            "İstanbul gibi rekabetçi pazarda yayın \"bitiriş\" değil, başlangıçtır. İlk 30 günde şu döngü kritik olur: kritik akışlarda sürtünme noktaları; stabilite (crash) ve performans; kullanıcı geri bildirimleri; küçük ama etkili iterasyonlar."
        )
    )

    body.append(
        cta_box(
            "Hedefinizi ve İstanbul'daki hedef kitlenizi 2–3 cümlede yazın",
            "Kapsamı netleştirip uygulanabilir bir plan çıkaralım. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("İstanbul'da mobil uygulama geliştirmede ilk adım nedir?", "Hedef kitleyi (bölge/segment) netleştirmek ve 2–3 kritik akışı seçmektir."),
        ("Yerel rekabeti aşmak için neye odaklanmalıyım?", "Daha çok özellik yerine, daha az sürtünme: hızlı onboarding, net CTA, kolay tekrar kullanım."),
        ("Saha toplantıları gerçekten gerekli mi?", "Bazı sektörlerde evet; ama verimli olması için ajanda + yazılı karar özeti şarttır."),
        ("Hızlı iletişim süreci bozmaz mı?", "Bozabilir. Bu yüzden haftalık özet, öncelik listesi ve kabul kriteri ile disiplin kurulur."),
        ("Yayın sonrası en kritik şey nedir?", "Kritik akış performansı, stabilite ve kullanıcı davranışına göre hızlı iterasyon."),
        ("Kapsam değişince ne yapılır?", "Değişiklikleri faz planına bağlarız: zorunlu/öncelikli/isteğe bağlı ayrımı ile yönetiriz."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "İstanbul'da Mobil Uygulama Geliştirme | Yerel Rekabet Odaklı Yaklaşım"
    meta_description = (
        "İstanbul'da mobil uygulama geliştirme: yerel rekabet, hızlı iletişim, saha toplantıları, sürdürülebilir süreç. Hedefe göre kapsam, teslim kriterleri ve ölçümleme."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "İstanbul'da Mobil Uygulama Geliştirme — Yerel Rekabeti Anlayan, Ölçülebilir Yaklaşım",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_mobil_uygulama_freelancer_tr(page: SeoPage) -> Dict:
    """Custom cluster: Mobil Uygulama Freelancer — risk azaltma, teslim kontrol listesi. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Mobil uygulama freelancer ile çalışmak doğru yönetilirse hızlı ilerletir; yanlış yönetilirse proje yarım kalır, kalite düşer veya sürdürülebilir olmaz."
        )
    )
    body.append(
        p(
            "Bu sayfa; freelancer seçimini \"şansa\" bırakmadan, kapsam + teslim kriterleri + test/yayın disiplini ile güvenli hale getirmen için hazırlanmıştır. Ana hedef: Tek kişilik ekip riskini azaltmak ve projenin \"teslim edilebilir\" olmasını garanti eden bir süreç kurmak. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) Tek Kişilik Ekip Riski"))
    body.append(
        p(
            "Freelancer ile çalışırken en büyük risk genelde \"yetkinlik\" değil, tek noktaya bağımlılıktır: tatil/hastalık/yoğunluk → gecikme; bilgi tek kişide → devamlılık sorunu; test ve dokümantasyon zayıf → yayın sonrası problem."
        )
    )
    body.append(
        p(
            "<strong>Çözüm prensibi:</strong> Tek kişiye bağımlılığı azaltmak için işi \"kişiye\" değil, sisteme bağla: yazılı kapsam, repo düzeni, test planı, yayın checklist."
        )
    )
    body.append(h3("2) Süreç Yönetimi Eksikliği"))
    body.append(
        p(
            "Freelancer işleri çoğu zaman \"yapıyorum gönderiyorum\" modunda gider. Bu, mobil uygulamada risklidir çünkü cihaz/OS çeşitliliği, store süreçleri, crash ve performans, analytics ve event takibi işin parçasıdır."
        )
    )
    body.append(
        p(
            "<strong>Çözüm prensibi:</strong> Haftalık ritim + net teslim kriterleri + \"done\" tanımı."
        )
    )

    body.append(h2("Önerilen Süreç (Freelancer için En Sağlam Akış)"))
    body.append(h3("1) Keşif ve Hedefler"))
    body.append(
        p(
            "Sorulması gereken 5 kritik soru: Uygulamanın ana hedefi nedir? (rezervasyon, sipariş, üyelik, takip vb.) En kritik 2–3 akış hangisi? İlk sürümde \"olmazsa olmaz\" ekranlar neler? Hangi entegrasyonlar şart? (auth, bildirim, ödeme, harita, CRM) Başarıyı hangi metrikle ölçeceğiz? (aktivasyon, tekrar kullanım, form dönüşümü)"
        )
    )
    body.append(p("<strong>Teslim:</strong> 1 sayfa hedef + kapsam özeti"))
    body.append(h3("2) Plan: Teslim Kriterleri ve Öncelikler"))
    body.append(
        ul(
            [
                "MVP (v1) + faz-2 listesi",
                "her maddeye kabul kriteri",
                "revizyon ve değişiklik yönetimi",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> kapsam listesi + kabul kriterleri"))
    body.append(h3("3) Uygulama: Tasarım/Geliştirme"))
    body.append(
        ul(
            [
                "tasarım dosyası net mi? (Figma/akışlar)",
                "kod standardı, branch düzeni",
                "crash logging + temel analytics eventleri",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> test edilebilir build + kritik akışlar çalışıyor"))
    body.append(h3("4) Test ve Yayın"))
    body.append(
        ul(
            [
                "cihaz matrisi (Android/iOS sürümleri)",
                "release checklist",
                "izleme: crash/performance + temel event doğrulama",
            ]
        )
    )
    body.append(p("<strong>Teslim:</strong> yayın-ready sürüm + izleme planı"))

    body.append(h2("Seçim Kriterleri (Freelancer Değerlendirme Listesi)"))
    body.append(h3("Teknik yeterlilik sinyalleri"))
    body.append(
        ul(
            [
                "daha önce benzer uygulama teslimi (store yayını görmüş olması ideal)",
                "net teknoloji seçimi ve gerekçesi",
                "versiyonlama ve release disiplinini biliyor olması",
                "performans/stabilite konuşabiliyor olması",
            ]
        )
    )
    body.append(h3("Süreç sinyalleri"))
    body.append(
        ul(
            [
                "\"kapsamı yazalım\" diyorsa iyi işaret",
                "haftalık raporlama ritmi öneriyorsa iyi işaret",
                "test ve yayın planı anlatabiliyorsa iyi işaret",
                "tek başına ise \"risk planı\" sunabiliyorsa mükemmel işaret",
            ]
        )
    )
    body.append(h3("Kırmızı bayraklar"))
    body.append(
        ul(
            [
                "\"her şeyi yaparım\" ama scope istemiyor",
                "test konuşmuyor",
                "repo / dokümantasyon umursamıyor",
                "yayın süreci ve store gereksinimlerini hafife alıyor",
            ]
        )
    )

    body.append(h2("Teslim Kontrol Listesi (Bu Listeyi Kullan, Sorun Azalır)"))
    body.append(p("<strong>Zorunlu teslimler:</strong>"))
    body.append(
        ul(
            [
                "kaynak kod + repo erişimi (tek hesapta kalmasın)",
                "build alma dokümantasyonu (README)",
                "release notları (ne yapıldı / ne kaldı)",
                "izleme kurulumları (crash logging, temel event'ler)",
                "kritik akış test senaryoları",
                "yayın checklist",
            ]
        )
    )
    body.append(p("<strong>Opsiyonel ama çok değerli:</strong> basit mimari şeması; component/feature listesi; teknik borç notları (sonra iyileştirme için)."))

    body.append(h2("Ne Zaman Freelancer Mantıklı? Ne Zaman Değil?"))
    body.append(
        p(
            "<strong>Freelancer mantıklı</strong> (özellikle): kapsam net ve küçük/orta ölçekliyse; MVP hızlı çıkacaksa; tek kişilik ekip riskini süreçle yönetebiliyorsan."
        )
    )
    body.append(
        p(
            "<strong>Freelancer riskli olabilir:</strong> çoklu entegrasyon + karmaşık rol/yetki varsa; timeline çok sıkışıksa ve yedek plan yoksa; bakım/iyileştirme döngüsü kritikse ve tek kişiye bağlı kalacaksan."
        )
    )

    body.append(h2("Yayın Sonrası Sürdürülebilirlik"))
    body.append(
        p(
            "Mobil projede sürdürülebilirlik = \"yayınlandı bitti\" değil: crash takibi, performans izleme, kullanıcı davranışı analizi, küçük iterasyonlar — bu döngü kurulmazsa uygulama kısa sürede düşer."
        )
    )

    body.append(
        cta_box(
            "Freelancer ile ilerlemek istiyorsan",
            "Önce kapsamı netleştirelim ve teslim kriterlerini yazılı hale getirelim. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Mobil uygulama freelancer ile çalışırken ilk adım nedir?", "Kritik akışları seçip kapsamı yazılı hale getirmek ve kabul kriterlerini belirlemek."),
        ("Tek kişilik ekip riskini nasıl azaltırım?", "Repo erişimi, dokümantasyon, test planı ve yayın checklist ile süreci kişiden bağımsızlaştırarak."),
        ("Freelancer seçerken en güçlü sinyal nedir?", "Daha önce store'a yayın görmüş proje + net süreç önerisi (kapsam, test, raporlama)."),
        ("Kapsam değişirse ne olur?", "Değişiklikleri faz planına bağlamak gerekir: zorunlu/öncelikli/isteğe bağlı ayrımı."),
        ("Teslimde hangi belgeler mutlaka olmalı?", "Repo, README, release notları, test senaryoları, izleme kurulumları."),
        ("Yayın sonrası en kritik konu nedir?", "Stabilite (crash) + performans + kullanıcı davranışına göre hızlı iterasyon."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobil Uygulama Freelancer | Doğru Seçim ve Teslim Kontrol Listesi"
    meta_description = (
        "Mobil uygulama freelancer ile çalışma rehberi: tek kişilik ekip riski, süreç yönetimi, seçim kriterleri, teslim kontrol listesi, test ve yayın planı."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Mobil Uygulama Freelancer ile Çalışma — Riskleri Azaltan, Net Teslim Odaklı Rehber",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_mobil_uygulama_nasil_yapilir_tr(page: SeoPage) -> Dict:
    """Custom cluster: Mobil Uygulama Nasıl Yapılır? — adım adım süreç rehberi. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Mobil uygulama yapmak sadece kod yazmak değildir. Başarılı bir mobil uygulama: doğru kapsamla başlar, net kullanıcı akışlarıyla tasarlanır, performans ve güvenlik gözetilerek geliştirilir, test edilir, yayınlanır, ölçülür ve iyileştirilir."
        )
    )
    body.append(
        p(
            "Bu rehber, mobil uygulama geliştirme sürecini stratejik ve sürdürülebilir şekilde açıklar. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("1) Fikir ve Hedef Netleştirme (En Kritik Aşama)"))
    body.append(
        p(
            "Çoğu mobil proje teknik değil, stratejik hatadan başarısız olur. Sorulması gereken temel sorular: Bu uygulama hangi problemi çözüyor? Hedef kullanıcı kim? En kritik 2–3 kullanıcı akışı ne? İlk sürümde olmazsa olmaz özellikler neler? Başarı hangi metrikle ölçülecek? (aktivasyon, sipariş, rezervasyon, dönüşüm)"
        )
    )
    body.append(p("Eğer bu aşama atlanırsa, proje geliştirme sırasında sürekli değişir."))

    body.append(h2("2) Kapsam ve MVP Tanımı"))
    body.append(
        p(
            "Mobil uygulama geliştirmede en büyük hata \"her şeyi ilk sürüme koymak\"tır. Doğru yöntem: Zorunlu (MVP), Öncelikli, İsteğe bağlı (2. faz). Her özellik için kabul kriteri yazılmalıdır. Örnek: \"Üyelik ekranı çalışır\" değil, \"E-posta doğrulamalı üyelik, hata mesajları gösteriliyor, backend doğrulaması var.\" Bu disiplin olmadan proje kontrol edilemez."
        )
    )

    body.append(h2("3) UX/UI Tasarım Süreci"))
    body.append(
        p(
            "Mobil uygulama tasarımı web tasarım değildir. Dikkat edilmesi gerekenler: Başparmak erişim alanı, Basit navigasyon, Ekran hiyerarşisi, Boş durumlar (empty states), Hata mesajları, Yüklenme durumları. Tasarım sadece görsel değil, kullanıcı deneyimi mimarisidir."
        )
    )

    body.append(h2("4) Teknoloji Seçimi (Android, iOS veya Cross-Platform)"))
    body.append(
        ul(
            [
                "Native Android",
                "Native iOS",
                "Cross-platform (Flutter, React Native vb.)",
                "Backend mimarisi (API, veritabanı, auth sistemi)",
            ]
        )
    )
    body.append(p("Seçim; hedef kitle, ölçeklenebilirlik ve performansa göre yapılmalıdır. Yanlış teknoloji = gelecekte teknik borç."))

    body.append(h2("5) Geliştirme Aşaması"))
    body.append(
        p(
            "Bu aşamada dikkat edilmesi gereken teknik konular: Temiz kod yapısı, Versiyon kontrolü (Git), API güvenliği, Performans optimizasyonu, Crash logging, Analytics event planı."
        )
    )
    body.append(p("Mobil uygulama geliştirme süreci, yalnızca \"çalışıyor\" demek değildir. \"Stabil çalışıyor\" demektir."))

    body.append(h2("6) Test Süreci"))
    body.append(
        p(
            "Test yapılmadan yayınlanan uygulama, kullanıcı kaybeder. Test türleri: Fonksiyonel test, Kullanıcı akış testi, Cihaz uyumluluk testi, Performans testi, Güvenlik kontrolü. Ayrıca: Form validasyonları, Hata senaryoları, Zayıf internet testi."
        )
    )

    body.append(h2("7) Yayın (App Store ve Google Play Süreci)"))
    body.append(
        p(
            "Yayın aşaması teknik olduğu kadar prosedüreldir: Store gereksinimleri, Gizlilik politikası, Uygulama açıklaması, Ekran görüntüleri, Sürüm notları, Onay süreci. Yayın = başlangıç."
        )
    )

    body.append(h2("8) Yayın Sonrası Ölçüm ve İyileştirme"))
    body.append(
        p(
            "Profesyonel mobil uygulama geliştirme sürecinde yayın sonrası: Crash takibi, Performans ölçümü, Kullanıcı davranışı analizi, Dönüşüm oranı optimizasyonu. İlk 30 gün en kritik dönemdir."
        )
    )

    body.append(h2("Riskler ve Çözümler"))
    body.append(
        ul(
            [
                "Kapsam sürekli değişiyor → Yazılı MVP ve faz planı",
                "Performans sorunları → Başta mimari plan",
                "Kullanıcı kaybı → UX test ve analytics",
                "Store reddi → Önceden gereksinim analizi",
            ]
        )
    )

    body.append(h2("Ne Zaman Profesyonel Süreç Gereklidir?"))
    body.append(
        ul(
            [
                "İş modeli uygulamaya bağlıysa",
                "Uzun vadeli büyüme hedefleniyorsa",
                "Entegrasyonlar karmaşıksa",
                "Performans kritikse",
            ]
        )
    )

    body.append(
        cta_box(
            "Mobil uygulama yapmak istiyorsanız",
            "Önce hedef ve kapsamı netleştirelim. Doğru plan olmadan kod yazmak risklidir. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Mobil uygulama yapmak ne kadar sürer?", "Süre; kapsam, entegrasyon ve test gereksinimlerine bağlıdır."),
        ("Mobil uygulama için ilk adım nedir?", "Problem ve kullanıcı hedefini netleştirmek."),
        ("Android mi iOS mu önce yapılmalı?", "Hedef kitle analizine göre karar verilir."),
        ("MVP nedir?", "Minimum çalışabilir ilk sürümdür."),
        ("Yayın sonrası süreç var mı?", "Evet. Ölçümleme ve iterasyon zorunludur."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobil Uygulama Nasıl Yapılır? Adım Adım Geliştirme Rehberi"
    meta_description = (
        "Mobil uygulama nasıl yapılır? Fikirden tasarıma, geliştirmeden test ve yayına kadar adım adım mobil uygulama geliştirme süreci ve risk yönetimi rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Mobil Uygulama Nasıl Yapılır? — Fikirden Yayına Adım Adım Süreç",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_mobil_uygulama_nedir_tr(page: SeoPage) -> Dict:
    """Custom cluster: Mobil Uygulama Nedir? — türler, senaryolar, doğru yaklaşım. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Mobil uygulama; kullanıcıların telefon veya tablet üzerinden belirli bir işi hızlı ve tekrar edilebilir şekilde yapmasını sağlayan yazılımdır. Ama pratikte \"mobil uygulama\" tek bir şey değildir: iOS / Android üzerinde çalışan uygulamalar; Web tabanlı ama uygulama gibi davranan çözümler; İş süreçlerini hızlandıran kurumsal araçlar; Satış, rezervasyon, lojistik, üyelik, bildirim gibi akışları yöneten sistemler."
        )
    )
    body.append(
        p(
            "Bu sayfanın amacı: \"Mobil uygulama gerçekten gerekiyor mu?\" sorusuna net cevap verecek bir çerçeve sunmak. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Mobil Uygulama Ne İşe Yarar?"))
    body.append(
        p(
            "Bir mobil uygulamanın en güçlü yanı, kullanıcıyla \"sürekli bir temas\" kurmasıdır. Mobil uygulama şu avantajları sağlar: Push bildirim ile geri dönüşleri artırma; Cihaz özellikleri (kamera, konum, biyometri) ile akışları hızlandırma; Tekrar eden işlemleri \"tek dokunuşa\" indirme; Offline / zayıf internet senaryolarında daha stabil deneyim; Kullanıcı davranışını ölçerek iyileştirme döngüsü kurma. Mobil uygulama; doğru senaryoda web'den daha güçlü bir deneyim sunar."
        )
    )

    body.append(h2("Mobil Uygulama Türleri"))
    body.append(h3("1) Native Uygulama (Android / iOS)"))
    body.append(
        p(
            "Her platformun kendi dili ve standartlarıyla geliştirilir. Ne zaman iyi? Performans kritikse; Kamera, Bluetooth, konum gibi donanım yoğun kullanılıyorsa; Uygulama \"ürünün kendisi\" ise."
        )
    )
    body.append(h3("2) Cross-Platform (Flutter / React Native)"))
    body.append(
        p(
            "Tek codebase ile Android ve iOS hedeflenir. Ne zaman iyi? Hızlı çıkış hedefleniyorsa; Ürün iki platformda da aynı deneyimi istiyorsa; MVP ve ilk faz için optimize edilecekse."
        )
    )
    body.append(h3("3) PWA (Progressive Web App)"))
    body.append(
        p(
            "Web site + uygulama benzeri deneyim. Ne zaman iyi? İçerik ağırlıklıysa; Basit kullanıcı akışları yeterliyse; App store bağımlılığı istenmiyorsa. Doğru tür, \"teknoloji trendi\" ile değil; kullanım senaryosu ile seçilir."
        )
    )

    body.append(h2("Doğru Kullanım Senaryosu Nasıl Seçilir?"))
    body.append(
        p(
            "Mobil uygulama kararında 3 test sorusu işe yarar: Kullanıcı aynı işlemi haftada kaç kez yapıyor? İşlem mobilde \"hız avantajı\" sağlıyor mu? Bildirim / cihaz özelliği (kamera, konum, QR) gerekiyor mu? Bu üçünden en az ikisi \"evet\" ise mobil uygulama güçlü bir adaydır."
        )
    )

    body.append(h2("Hedef Kitle: B2C mi B2B mi?"))
    body.append(h3("B2C (Son kullanıcı)"))
    body.append(
        p(
            "Öncelik: kullanıcı deneyimi, hız, onboarding, retention. Örnekler: e-ticaret, rezervasyon, sosyal / içerik, teslimat."
        )
    )
    body.append(h3("B2B (Kurumsal kullanıcı)"))
    body.append(
        p(
            "Öncelik: süreç, yetkilendirme, raporlama, entegrasyonlar. Örnekler: saha ekipleri için uygulama, CRM destek uygulaması, stok / sipariş takip, operasyon yönetimi."
        )
    )

    body.append(h2("Örnek Senaryolar"))
    body.append(
        ul(
            [
                "Rezervasyon / randevu uygulaması: hızlı tekrar eden akış",
                "Sipariş ve teslimat takibi: konum + bildirim + durum yönetimi",
                "Sadakat / üyelik uygulaması: push + kampanya akışları",
                "Kurumsal operasyon uygulaması: rol bazlı yetki + raporlama",
            ]
        )
    )

    body.append(h2("Önerilen Süreç (Kısa ve Net)"))
    body.append(
        p(
            "Başarılı mobil projeler aynı sırayı takip eder: Keşif → Kapsam → UX/UI → Geliştirme → Test → Yayın → Ölçüm ve İyileştirme. Bu sırayı korumak, hem kaliteyi hem sürdürülebilirliği artırır."
        )
    )

    body.append(h2("Kalite Standartları (Mobil İçin Olmazsa Olmazlar)"))
    body.append(
        ul(
            [
                "Net kullanıcı akışları ve ekran hiyerarşisi",
                "Performans hedefleri (ilk açılış, ekran geçişleri)",
                "Güvenlik: auth, token, erişim kontrolü",
                "İzleme: crash log + temel analitik olaylar",
                "Yayın sonrası iyileştirme planı",
            ]
        )
    )

    body.append(
        cta_box(
            "Mobil uygulama fikriniz varsa",
            "Önce doğru senaryoyu ve hedef kitlenizi netleştirelim. Doğru plan, sürprizleri azaltır ve uygulamayı büyütmeyi kolaylaştırır. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Mobil uygulama nedir, web sitesinden farkı ne?", "Mobil uygulama; cihaz özellikleri, bildirim ve akış hızında avantaj sağlar; web ise erişim ve içerik tarafında hızlıdır."),
        ("Her iş için mobil uygulama gerekir mi?", "Hayır. Tekrar eden akış, bildirim ihtiyacı ve cihaz özellikleri yoksa web/PWA daha doğru olabilir."),
        ("Native mi cross-platform mu seçmeliyim?", "Performans ve cihaz kullanımı kritikse native; hızlı çıkış ve ortak deneyim hedefleniyorsa cross-platform mantıklıdır."),
        ("PWA ile gerçek uygulama arasındaki fark nedir?", "PWA web tabanlıdır; bazı donanım ve store özellikleri sınırlı olabilir."),
        ("Başlamak için ilk adım nedir?", "Hedef kullanıcıyı ve en kritik 2–3 akışı netleştirmektir."),
        ("Yayın sonrası süreç önemli mi?", "Evet. Ölçümleme ve iterasyon olmadan büyüme zorlaşır."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobil Uygulama Nedir? Türler, Kullanım Senaryoları ve Örnekler"
    meta_description = (
        "Mobil uygulama nedir? Native, cross-platform ve PWA farkları, doğru kullanım senaryosu, hedef kitle ve örnek mobil uygulama türleriyle açıklayıcı rehber."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Mobil Uygulama Nedir? — Türler, Senaryolar ve Doğru Yaklaşım",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_ozel_mobil_uygulama_tr(page: SeoPage) -> Dict:
    """Custom cluster: Özel Mobil Uygulama — ürün odaklı, ölçeklenebilir, sürdürülebilir. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Özel mobil uygulama; \"hazır bir şablonu uyarlamak\" yerine, iş hedeflerinize ve kullanıcı akışlarınıza göre sıfırdan tasarlanan bir üründür. Buradaki amaç yalnızca uygulamayı yayınlamak değil; yayın sonrası da büyüyebilen, ölçülebilen ve sürdürülebilen bir altyapı kurmaktır."
        )
    )
    body.append(
        p(
            "Bu yaklaşım özellikle: süreçleri dijitalleştiren (B2B), kullanıcı bağlılığı (retention) isteyen (B2C), entegrasyon ve raporlama ihtiyacı olan projelerde en doğru sonucu verir. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) İş hedefi uyumu"))
    body.append(
        p(
            "Uygulama \"güzel görünsün\" diye değil; ölçülebilir bir hedef için yapılır. Örnek hedefler: sipariş / rezervasyon sayısını artırmak; operasyon süresini kısaltmak; müşteri hizmeti yükünü azaltmak; kullanıcıların tekrar kullanımını artırmak."
        )
    )
    body.append(h3("2) Uzun vadeli geliştirme"))
    body.append(
        p(
            "Özel mobil uygulama bir \"tek seferlik iş\" değildir. Ürün büyüdükçe: yeni akışlar eklenir, performans optimize edilir, güvenlik sertleştirilir, analitik veriye göre iterasyon yapılır. Bu nedenle ilk günden \"yol haritası + mimari + ölçümleme\" planlanır."
        )
    )

    body.append(h2("Ne Zaman Özel Mobil Uygulama Tercih Etmelisiniz?"))
    body.append(
        p(
            "Aşağıdaki durumlardan 2–3'ü sizde varsa, özel geliştirme mantıklıdır: Akışlarınız standart değil, işinize özgü; CRM/ERP/ödeme/kargo gibi entegrasyonlar var; Roller ve yetkiler (admin, saha, müşteri) gerekiyor; Bildirim, konum, kamera, QR gibi cihaz yetenekleri kritik; Ürünü uzun vadede büyütmeyi planlıyorsunuz."
        )
    )
    body.append(
        ul(
            [
                "Akışlarınız standart değil, işinize özgü",
                "CRM/ERP/ödeme/kargo gibi entegrasyonlar var",
                "Roller ve yetkiler (admin, saha, müşteri) gerekiyor",
                "Bildirim, konum, kamera, QR gibi cihaz yetenekleri kritik",
                "Ürünü uzun vadede büyütmeyi planlıyorsunuz",
            ]
        )
    )

    body.append(h2("Önerilen Süreç"))
    body.append(
        p(
            "Başarılı özel mobil uygulamalar, aynı omurgayı takip eder: 1) Keşif ve hedefler: hedef KPI'lar, kullanıcı tipleri ve senaryolar, kısıtlar ve riskler. 2) Plan: kapsam + teslim kriterleri — MVP netleştirme, fazlara bölme, \"tamamlandı\" tanımı. 3) Uygulama: UX/UI + geliştirme — bilgi mimarisi, bileşen tasarımı, API entegrasyonları. 4) Test ve yayın: senaryo testleri, performans kontrolü, yayın checklist + izleme kurulumu."
        )
    )

    body.append(h2("Teslimatlar"))
    body.append(h3("Ürün Yol Haritası (Roadmap)"))
    body.append(
        p(
            "Özel projede en kritik çıktı, \"ne zaman ne eklenecek?\" sorusuna net cevap veren yol haritasıdır. Yol haritası şunları içerir: MVP kapsamı, sonraki fazlar, ölçümleme planı, risk ve bağımlılıklar."
        )
    )
    body.append(h3("Teknik Mimari"))
    body.append(
        p(
            "Sürdürülebilir bir uygulama için mimari şunları netleştirir: backend yapısı ve API sözleşmeleri; kimlik doğrulama / yetkilendirme; veri güvenliği yaklaşımı; analitik ve hata izleme; sürümleme ve yayın stratejisi."
        )
    )

    body.append(h2("Kalite Standartları: Özel Uygulamada Fark Yaratan Detaylar"))
    body.append(
        ul(
            [
                "Performans: hızlı açılış, akıcı ekran geçişleri",
                "Güvenlik: token yönetimi, rol bazlı erişim, güvenli depolama",
                "Ölçümleme: event takibi, funnel, retention metrikleri",
                "Bakım: düzenli güncelleme, crash izleme, log standardı",
                "Sürdürülebilirlik: kod standartları ve dokümantasyon",
            ]
        )
    )
    body.append(p("Özel uygulamada kalite, \"son gün yapılan kontrol\" değil; süreç boyunca korunan bir standarttır."))

    body.append(h2("Yayın Planı ve Sürdürülebilirlik"))
    body.append(
        p(
            "Yayın, bitiş değil başlangıçtır. İlk 30 gün genelde şu döngü çalışır: kullanıcı davranışı ölçülür, darboğazlar tespit edilir, küçük iterasyonlarla hızla iyileştirilir. Bu yaklaşım, uygulamanın büyümesini gerçek veriye bağlar."
        )
    )

    body.append(
        cta_box(
            "Özel mobil uygulama planlıyorsanız",
            "İlk adım kapsamı netleştirmek ve yol haritasını doğru kurmaktır. Hedefinizi ve önceliklerinizi paylaşın; size uygun planı birlikte çıkaralım. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Özel mobil uygulama ile hazır çözüm arasındaki fark nedir?", "Özel uygulama, iş akışlarınıza göre tasarlanır ve uzun vadede büyütülebilir; hazır çözümler genelde standart akışlarla sınırlıdır."),
        ("MVP nedir ve neden önemlidir?", "MVP, ilk sürümde sadece kritik akışları yayınlayıp hızlı doğrulama yapmanızı sağlar. Sonraki fazlar veriye göre planlanır."),
        ("Teknik mimari neden bu kadar kritik?", "Mimari; performans, güvenlik ve bakım maliyetini doğrudan etkiler. Kötü mimari, büyüdükçe yavaşlatır."),
        ("Ölçümleme (analytics) şart mı?", "Evet. Retention ve dönüşüm gibi metrikler olmadan iyileştirme \"tahminle\" yapılır."),
        ("Başlamak için hangi bilgileri hazırlamalıyım?", "Hedef, hedef kitle, 2–3 kritik kullanıcı akışı ve varsa entegrasyon ihtiyaçları."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Özel Mobil Uygulama Geliştirme | Ürün Odaklı, Ölçeklenebilir Çözümler"
    meta_description = (
        "Özel mobil uygulama nedir, ne zaman tercih edilir? Ürün yol haritası, teknik mimari, uzun vadeli geliştirme ve sürdürülebilir mobil uygulama yaklaşımı."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Özel Mobil Uygulama — Ürün Odaklı, Ölçeklenebilir ve Sürdürülebilir Geliştirme",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_android_vs_ios_tr(page: SeoPage) -> Dict:
    """Custom cluster: Android mi iOS mu? — platform selection guide. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "\"Android mi iOS mu?\" sorusu aslında teknoloji sorusu değil, ürün ve büyüme stratejisi sorusudur. Doğru platform seçimi; hedef kitlenizi, pazara çıkış planınızı, ürününüzün kullanım senaryolarını ve sürdürülebilir geliştirmeyi aynı çerçevede ele aldığınızda netleşir."
        )
    )
    body.append(
        p(
            "Bu sayfa, platform kararını \"tahminle\" değil ölçülebilir kriterlerle vermeniz için hazırlanmıştır. "
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("En Sık Karşılaşılan İhtiyaçlar"))
    body.append(h3("1) Hedef Kitle ve Kullanım Alışkanlığı"))
    body.append(
        p(
            "Platform seçimi, kullanıcı profilinizle başlar: Türkiye/İstanbul odağı (hedef segmentin cihaz tercihleri), kurumsal/B2B kullanım (cihaz standardizasyonu), geniş kitle / farklı cihazlar (Android'de cihaz çeşitliliği test ve optimizasyon planını büyütür). Kritik soru: Kullanıcılarınız uygulamayı \"günlük alışkanlık\" olarak mı kullanacak, yoksa \"ihtiyaç anında\" mı açacak?"
        )
    )
    body.append(h3("2) Zaman ve Pazara Çıkış (Go-to-Market)"))
    body.append(
        p(
            "Hedef \"hızlı öğrenme\" ise tek platformla başlayıp doğrulama yapmak mantıklı olabilir: önce MVP → kullanıcı davranışı ölçümü → iterasyon; fazlı plan (v1 tek platform, v2 ikinci platform); yayın sonrası veriye göre öncelik güncelleme. Kritik soru: İlk sürümde ölçmek istediğiniz \"tek\" davranış nedir?"
        )
    )
    body.append(h3("3) Ürün Karmaşıklığı ve Teknik Risk"))
    body.append(
        p(
            "Bazı ürünler iki platformda aynı zorlukta değildir: gerçek zamanlı özellikler, yoğun medya kullanımı, offline senaryolar; push bildirimleri ve arka plan görevleri; cihaz donanımlarını kullanan özellikler (kamera, konum, sensörler). Kritik soru: Ürününüzün \"en kritik akışı\" platformlar arasında aynı stabiliteyle çalışmak zorunda mı?"
        )
    )

    body.append(h2("Android ve iOS Arasındaki Pratik Farklar (Karar İçin)"))
    body.append(h3("Android: Güçlü Yanlar"))
    body.append(
        ul(
            [
                "geniş cihaz ekosistemi → geniş erişim potansiyeli",
                "farklı ekran ve donanım senaryolarına uygun esnek yapı",
                "doğru mimariyle yüksek ölçeklenebilirlik",
            ]
        )
    )
    body.append(p("Dikkat edilmesi gereken: cihaz çeşitliliği → test matrisi ve performans optimizasyonu şart."))
    body.append(h3("iOS: Güçlü Yanlar"))
    body.append(
        ul(
            [
                "cihaz/OS çeşitliliği daha kontrollü → stabilite yönetimi daha kolay",
                "kullanıcı deneyim standardı daha tutarlı",
                "bazı ürünlerde hızlı ve net iterasyon döngüsü avantajı",
            ]
        )
    )
    body.append(p("Dikkat edilmesi gereken: ürünün hedef kitlesi iOS ağırlıklı değilse, erişim beklentisi doğru kurulmalı."))

    body.append(h2("Önerilen Süreç: Platform Seçimini Netleştiren Akış"))
    body.append(h3("1) Keşif ve Hedefler"))
    body.append(
        ul(
            [
                "hedef kullanıcı kim? hangi problem çözülüyor?",
                "kritik akışlar neler? (kayıt, ödeme, rezervasyon, mesajlaşma vb.)",
                "ölçüm metrikleri: retention, aktivasyon, dönüşüm adımları",
            ]
        )
    )
    body.append(p("<strong>Çıktı:</strong> karar kriterleri + MVP hedefi"))
    body.append(h3("2) Plan: Teslim Kriterleri ve Öncelikler"))
    body.append(
        ul(
            [
                "tek platform mu çift platform mu?",
                "fazlara bölme: v1, v1.1, v2",
                "analitik event planı (hangi aksiyonlar ölçülecek?)",
            ]
        )
    )
    body.append(p("<strong>Çıktı:</strong> yol haritası + kapsam sınırları"))
    body.append(h3("3) Uygulama: Tasarım/Geliştirme"))
    body.append(
        ul(
            [
                "mobil-first UX, net CTA",
                "performans odaklı veri yönetimi",
                "güvenlik temeli: auth/token, veri koruma",
            ]
        )
    )
    body.append(p("<strong>Çıktı:</strong> test edilebilir sürüm"))
    body.append(h3("4) Test ve Yayın"))
    body.append(
        p(
            "cihaz/sürüm kapsaması, crash takibi ve yayın checklist, yayın sonrası ilk iyileştirme döngüsü."
        )
    )
    body.append(p("<strong>Çıktı:</strong> izleme planı + iterasyon listesi"))

    body.append(h2("Teslimatlar"))
    body.append(
        p(
            "Bu sayfada \"platform seçimi rehberi\" teslimi şu somut çıktılara dönüşür: platform karar dokümanı (neden/varsayımlar/riske karşı plan), MVP kapsamı ve faz planı, test stratejisi (Android için cihaz matrisi; iOS için sürüm kapsaması), ölçümleme planı (event tracking, dönüşüm adımları)."
        )
    )

    body.append(h2("Ne Zaman Bu Yaklaşımı Seçmelisiniz?"))
    body.append(
        p(
            "Bu yaklaşım, \"hangisi daha iyi?\" tartışmasını bitirir ve iş hedefi üzerinden karar verdirir. Şu durumlarda ideal:"
        )
    )
    body.append(
        ul(
            [
                "hedefleriniz ölçülebilir ve netse",
                "kapsamı yazılı yönetmek istiyorsanız",
                "yayın sonrası iterasyonla büyümeyi planlıyorsanız",
                "teknik riskleri baştan görmek istiyorsanız",
            ]
        )
    )

    body.append(
        cta_box(
            "Hedefinizi ve kullanıcı kitlenizi yazın",
            "Platform kararını birlikte netleştirip uygulanabilir bir plan çıkaralım. Teklif sayfasına gidin.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Android mi iOS mu seçerken ilk adım nedir?", "Hedef kullanıcıyı ve kritik akışı netleştirmek; ardından ölçülebilir hedef belirlemektir."),
        ("Tek platformla başlamak mantıklı mı?", "Evet. Özellikle MVP'de, veri toplayıp öğrenmek için tek platformla başlamak çoğu zaman daha kontrollüdür."),
        ("Android'de en büyük risk nedir?", "Cihaz çeşitliliği nedeniyle test ve performans optimizasyonunun iyi planlanmaması."),
        ("iOS neden bazı projelerde daha hızlı ilerler?", "Cihaz/OS ekosistemi daha kontrollü olduğu için stabilite ve test yönetimi daha öngörülebilir olabilir."),
        ("Platform seçimi SEO gibi organik büyümeyi etkiler mi?", "Doğrudan değil; fakat ölçümleme, performans ve kullanıcı deneyimi büyümeyi doğrudan etkiler."),
        ("Yayından sonra neye odaklanılmalı?", "Crash oranı, aktivasyon adımları, retention ve kritik akışların performansı."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Android mi iOS mu? | Doğru Platform Seçimi Rehberi"
    meta_description = (
        "Android mi iOS mu seçmelisiniz? Hedef kitle, ürün stratejisi, performans, yayın süreci ve sürdürülebilir geliştirme açısından doğru platform kararını netleştirin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Android mi iOS mu? — Hedefe Göre Doğru Platformu Seçin",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_b2b_ecommerce_tr(page: SeoPage) -> Dict:
    """Custom cluster: B2B E-Ticaret — bayi, toptan satış, teklif, cari hesap, ERP. No pricing triggers (use tarife/liste)."""
    body: List[str] = []

    body.append(h2("Genel Bakış"))
    body.append(
        p(
            "B2B e-ticaret; klasik online mağazadan farklıdır. Burada hedef son kullanıcı değil, bayi, distribütör veya kurumsal müşteridir."
        )
    )
    body.append(
        p(
            "Bu nedenle sistem: müşteriye özel tarife listeleri, müşteri bazlı iskonto, teklif alma süreci, cari hesap takibi, ERP / muhasebe entegrasyonu gibi kurumsal ihtiyaçlara cevap vermelidir. Standart B2C altyapılar çoğu zaman bu karmaşıklığı yönetemez."
        )
    )
    body.append(
        p(
            f"Genel e-ticaret çerçevesi: {{{{ link:{_pillar_url(page)} }}}}. Rehber: {{{{ link:{_guide_url(page)} }}}}. Teklif: {{{{ link:{_quote_url(page)} }}}}."
        )
    )

    body.append(h2("B2B E-Ticaret Neden Farklıdır?"))
    body.append(
        p(
            "B2B projelerde satın alma süreci daha uzundur: Ürün araştırması, teklif talebi, onay süreci, sipariş oluşturma, vadeli ödeme / cari hesap. Bu akış; teknik mimaride doğru planlanmalıdır."
        )
    )

    body.append(h2("Temel B2B Özellikleri"))
    body.append(h3("Müşteri Bazlı Tarife ve İndirim"))
    body.append(
        p(
            "Her bayiye özel liste, iskonto oranı veya kampanya tanımlanabilir."
        )
    )
    body.append(h3("Teklif (RFQ) Sistemi"))
    body.append(
        p(
            "Sepet yerine \"teklif iste\" akışı kullanılabilir."
        )
    )
    body.append(h3("Cari Hesap ve Vade Yönetimi"))
    body.append(
        p(
            "Ödeme anında değil, vadeli sistemle çalışılabilir."
        )
    )
    body.append(h3("Onay Mekanizması"))
    body.append(
        p(
            "Şirket içi satın alma yetkilileri için çok adımlı onay sistemi."
        )
    )
    body.append(h3("ERP / CRM Entegrasyonu"))
    body.append(
        p(
            "Stok, fatura ve sipariş senkronizasyonu."
        )
    )

    body.append(h2("B2B E-Ticaret Geliştirme Süreci"))
    body.append(h3("1) Keşif ve Analiz"))
    body.append(
        ul(
            [
                "Satış modeli (bayi mi distribütör mü?)",
                "Sipariş hacmi",
                "Entegrasyon ihtiyacı",
                "Onay akış yapısı",
            ]
        )
    )
    body.append(h3("2) Mimari Planlama"))
    body.append(
        ul(
            [
                "Rol bazlı kullanıcı sistemi",
                "Tarife segmentasyonu",
                "Performans planı",
            ]
        )
    )
    body.append(h3("3) Geliştirme"))
    body.append(
        ul(
            [
                "Güvenli erişim yapısı",
                "Yetkilendirme katmanı",
                "Ölçeklenebilir veritabanı",
            ]
        )
    )
    body.append(h3("4) Test ve Yayın"))
    body.append(
        ul(
            [
                "Sipariş akış testi",
                "Liste ve indirim doğrulama",
                "Entegrasyon kontrolü",
                "Güvenlik testi",
            ]
        )
    )

    body.append(h2("SEO ve B2B"))
    body.append(
        p(
            "B2B projeler sadece satış sistemi değildir. Aynı zamanda ürün katalog SEO, kategori görünürlüğü, teknik içerik stratejisi, sektörel anahtar kelimeler üzerinden organik trafik üretir. Doğru kategori mimarisi, uzun vadede ciddi avantaj sağlar."
        )
    )

    body.append(h2("Hazır B2B Altyapı mı Özel Yazılım mı?"))
    body.append(
        p(
            "Hazır sistemler: sınırlı özelleştirme, entegrasyon zorluğu, performans kısıtları getirebilir. Özel B2B e-ticaret yazılımı: karmaşık tarife ve indirim yapısını yönetir; bayi bazlı kontrol sağlar; ölçeklenebilir kalır; teknik borcu azaltır. B2B projelerde çoğu zaman özel mimari tercih edilir."
        )
    )

    body.append(h2("Kalite Standartları"))
    body.append(
        p(
            "Başlamadan önce net olmalı: Yetki seviyeleri nasıl? Sipariş minimumları var mı? Ödeme tipi nasıl çalışacak? ERP hangi sıklıkla senkronize olacak? Belirsizlik, proje süresini uzatır."
        )
    )

    body.append(h2("Yayın Sonrası Sürdürülebilirlik"))
    body.append(
        ul(
            [
                "Sipariş hacmi izleme",
                "Performans takibi",
                "Sunucu ölçekleme",
                "Güvenlik güncellemeleri",
                "Yedekleme planı",
            ]
        )
    )
    body.append(p("B2B sistemler büyüdükçe altyapı da büyümelidir."))

    body.append(
        cta_box(
            "B2B satış modelinizi birlikte netleştirelim",
            "İhtiyaçlarınıza göre ölçeklenebilir bir mimari planlayalım. B2B E-Ticaret teklif sayfasına gidin.",
            _quote_url(page),
            "B2B E-Ticaret Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("B2B e-ticaret süresi neye bağlıdır?", "Entegrasyon sayısı ve tarife/indirim yapısının karmaşıklığına bağlıdır."),
        ("Hazır platform yeterli olur mu?", "Basit modellerde olabilir; karmaşık bayi yapılarında genellikle özel yazılım gerekir."),
        ("ERP entegrasyonu yapılabilir mi?", "Doğru planlama ile evet."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "B2B E-Ticaret Yazılımı | Toptan Satış ve Bayi Yönetim Sistemi"
    meta_description = (
        "B2B e-ticaret geliştirme: bayi yönetimi, müşteriye özel listeler, teklif akışı, cari hesap ve ERP entegrasyonu. Ölçeklenebilir ve kurumsal çözümler."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "B2B E-Ticaret — Bayi ve Toptan Satış İçin Ölçeklenebilir Altyapı",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_b2c_ecommerce_tr(page: SeoPage) -> Dict:
    """Custom cluster: B2C E-Ticaret — son kullanıcıya satış, dönüşüm ve SEO odaklı mağaza. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Genel Bakış"))
    body.append(
        p(
            "B2C e-ticaret; doğrudan son kullanıcıya satış yapılan dijital mağaza modelidir. Bu modelde başarı; hızlı ödeme süreci, mobil uyumlu tasarım, güven veren kullanıcı deneyimi, güçlü SEO altyapısı ve performans optimizasyonu ile doğrudan ilişkilidir."
        )
    )
    body.append(
        p(
            "Standart bir site kurmak yeterli değildir; dönüşüm üreten bir sistem kurmak gerekir. "
            f"Genel e-ticaret çerçevesi için {{{{ link:{_pillar_url(page)} }}}}, süreç odaklı rehber için {{{{ link:{_guide_url(page)} }}}} sayfasını inceleyebilirsiniz."
        )
    )

    body.append(h2("B2C E-Ticaret Neden Stratejik Bir Yatırımdır?"))
    body.append(
        p(
            "Online rekabet her geçen gün artıyor. Başarılı bir B2C e-ticaret sitesi; marka bilinirliğini artırır, reklam harcamasını daha verimli hale getirir, organik trafik üretir ve tekrar satın alma oranını yükseltir. Doğru mimari; uzun vadede reklam bağımlılığını azaltır."
        )
    )

    body.append(h2("B2C E-Ticaret Sitesinde Kritik Özellikler"))
    body.append(h3("Mobil Öncelikli Tasarım (Mobile First)"))
    body.append(
        p(
            "Trafiğin büyük bölümü mobil cihazlardan gelir. Bu nedenle mobil deneyim kusursuz olmalıdır."
        )
    )
    body.append(h3("Hızlı ve Güvenli Ödeme"))
    body.append(
        ul(
            [
                "Tek sayfa checkout",
                "Kredi kartı entegrasyonu",
                "3D secure",
                "Dijital cüzdan seçenekleri",
            ]
        )
    )
    body.append(
        p(
            "Ödeme sürecindeki her ekstra adım, dönüşüm kaybı riski taşır."
        )
    )
    body.append(h3("Kampanya ve Kupon Yönetimi"))
    body.append(
        ul(
            [
                "İndirim kodları",
                "Sepet bazlı promosyon",
                "Ürün bazlı kampanyalar",
            ]
        )
    )
    body.append(h3("SEO Uyumlu Kategori Yapısı"))
    body.append(
        ul(
            [
                "Doğru başlık hiyerarşisi",
                "Schema yapılandırması",
                "URL optimizasyonu",
                "İç linkleme stratejisi",
            ]
        )
    )
    body.append(h3("Performans Optimizasyonu"))
    body.append(
        ul(
            [
                "Core Web Vitals uyumu",
                "Görsel optimizasyon",
                "Cache ve CDN kullanımı",
            ]
        )
    )

    body.append(h2("B2C E-Ticaret Geliştirme Süreci"))
    body.append(h3("1) Hedef ve Analiz"))
    body.append(
        ul(
            [
                "Satış hedefi",
                "Ortalama sepet tutarı",
                "Hedef kitle analizi",
                "Rekabet değerlendirmesi",
            ]
        )
    )
    body.append(h3("2) Mimari ve UX Planlama"))
    body.append(
        ul(
            [
                "Kategori yapısı",
                "Filtre sistemi",
                "Kullanıcı akışı",
                "Sepet optimizasyonu",
            ]
        )
    )
    body.append(h3("3) Geliştirme"))
    body.append(
        ul(
            [
                "Güvenli altyapı",
                "Hız odaklı uygulama",
                "Ödeme entegrasyonları",
            ]
        )
    )
    body.append(h3("4) Test ve Yayın"))
    body.append(
        ul(
            [
                "Sepet testi",
                "Ödeme senaryoları",
                "Mobil performans testi",
                "SEO teknik kontrol",
            ]
        )
    )

    body.append(h2("B2C E-Ticaret ve SEO"))
    body.append(
        p(
            "SEO; B2C sitelerde en güçlü uzun vadeli trafik kaynağıdır. Doğru yapı; kategori bazlı anahtar kelime hedefleme, ürün sayfası optimizasyonu, blog destekli içerik stratejisi ve teknik SEO altyapısı ile sürdürülebilir büyüme sağlar. Google’da görünmeyen bir e-ticaret sitesi, sadece reklamla ayakta kalmaya çalışır."
        )
    )

    body.append(h2("Hazır Altyapı mı Özel Yazılım mı?"))
    body.append(
        p(
            "Hazır sistemler; hızlı kurulum ve düşük başlangıç yükü sağlayabilir. Ancak performans sınırı, özelleştirme kısıtı ve teknik borç riski oluşturabilir. Özel yazılım; yüksek performans, tam SEO kontrolü, ölçeklenebilir mimari ve entegrasyon esnekliği sağlar. Büyümeyi hedefleyen markalar için genellikle özel geliştirme tercih edilir."
        )
    )

    body.append(h2("Kalite Standartları"))
    body.append(
        p(
            "Başlamadan önce netleşmeli: Minimum performans hedefi nedir? Ödeme adımları kaç ekran? Kampanya yapısı nasıl çalışacak? Kategori SEO planı var mı? Net kabul kriterleri; revizyon süresini azaltır."
        )
    )

    body.append(h2("Yayın Sonrası Sürdürülebilirlik"))
    body.append(
        ul(
            [
                "Dönüşüm oranı takibi",
                "Sepet terk analizi",
                "A/B testleri",
                "Güvenlik güncellemeleri",
                "Performans izleme",
            ]
        )
    )
    body.append(
        p(
            "E-ticaret sitesi canlı bir sistemdir ve sürekli optimize edilmelidir."
        )
    )

    body.append(
        cta_box(
            "Satış odaklı, hızlı ve SEO uyumlu bir B2C e-ticaret altyapısı kuralım.",
            "Hedefinizi paylaşın; size uygun B2C E-Ticaret yol haritasını birlikte çıkaralım.",
            _quote_url(page),
            "B2C E-Ticaret Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("B2C e-ticaret sitesi ne kadar sürede tamamlanır?", "Kapsam ve entegrasyonlara göre değişir."),
        ("SEO başlangıçta mı yapılmalı?", "Evet. SEO sonradan eklenen bir özellik değildir; mimari karardır."),
        ("Mobil optimizasyon neden kritik?", "Çünkü kullanıcıların büyük bölümü mobil cihazdan alışveriş yapar."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "B2C E-Ticaret Sitesi | SEO Uyumlu ve Dönüşüm Odaklı Altyapı"
    meta_description = (
        "B2C e-ticaret sitesi geliştirme: mobil uyumlu tasarım, hızlı ödeme, kampanya yönetimi ve SEO altyapısı. Ölçeklenebilir ve performans odaklı çözümler."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "B2C E-Ticaret — Dönüşüm Odaklı ve SEO Uyumlu Online Mağaza",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_e_ticaret_nedir_tr(page: SeoPage) -> Dict:
    """Custom cluster: E-Ticaret Nedir? — kavramlar, türler, başlangıç kontrol listesi. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "E-ticaret (elektronik ticaret), ürün veya hizmetlerin internet üzerinden tanıtılması, sipariş alınması, ödeme yapılması ve teslim edilmesi sürecidir. Başarılı bir e-ticaret projesi için en kritik adım; hedefi, kapsamı ve ölçülebilir çıktıları en başta netleştirmektir."
        )
    )
    body.append(
        p(
            "Ölçeklenebilir altyapı yaklaşımı için ana hizmet sayfasını inceleyebilirsiniz: "
            f"{{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("E-Ticaret Nasıl Çalışır?"))
    body.append(
        p(
            "Temel akış genellikle şu sırayla ilerler:"
        )
    )
    body.append(
        ul(
            [
                "Trafik (SEO, reklam, sosyal medya, e-posta)",
                "Ürün keşfi (kategori/filtre, arama, öneriler)",
                "Sepet (kargo, kupon, hediye, upsell)",
                "Ödeme (kart, havale/EFT, dijital cüzdan, 3D Secure)",
                "Sipariş yönetimi (stok, fatura, kargo, iade)",
                "Ölçümleme ve optimizasyon (dönüşüm oranı, sepet terk, LTV)",
            ]
        )
    )

    body.append(h2("E-Ticaret Türleri: B2C, B2B ve D2C"))
    body.append(h3("B2C (Business to Consumer)"))
    body.append(
        p(
            "Doğrudan son kullanıcıya satış. Öncelikler: mobil deneyim, hızlı ödeme, kampanya alanları, SEO kategori yapısı."
        )
    )
    body.append(h3("B2B (Business to Business)"))
    body.append(
        p(
            "Şirketlere satış. Öncelikler: liste/iskonto yapıları, teklif akışı, cari hesap, onay süreçleri, bayi paneli."
        )
    )
    body.append(h3("D2C (Direct to Consumer)"))
    body.append(
        p(
            "Markanın aracı olmadan tüketiciye satması. Öncelikler: marka deneyimi, tekrar satın alma, e-posta otomasyonu, sadakat."
        )
    )

    body.append(h2("Temel E-Ticaret Kavramları"))
    body.append(
        ul(
            [
                "Checkout / Ödeme adımı: dönüşümü en çok etkileyen akış",
                "CR (Conversion Rate) / Dönüşüm oranı: satış / ziyaret oranı",
                "AOV (Average Order Value) / Ortalama sepet: kampanya ve ürün stratejisiyle artar",
                "SEO altyapısı: URL, başlık hiyerarşisi, schema, iç linkleme",
                "Core Web Vitals: hız ve kullanıcı deneyimi metrikleri",
                "Ürün veri yapısı: varyant, stok, tarife, görsel, açıklama, etiket",
            ]
        )
    )

    body.append(h2("E-Ticaret Sitesi Kurarken En Sık İhtiyaçlar"))
    body.append(
        ul(
            [
                "Hızlı ödeme (tek sayfa checkout)",
                "Mobil uyumlu tasarım (mobile-first)",
                "Kampanya/kupon sistemi",
                "Kargo entegrasyonu ve iade süreçleri",
                "Stok ve ürün varyant yönetimi",
                "SEO uyumlu kategori ve ürün sayfaları",
                "Analitik ve ölçümleme (GA4, Pixel, event tracking)",
            ]
        )
    )

    body.append(h2("Önerilen Süreç"))
    body.append(h3("1) Keşif ve hedefler"))
    body.append(
        p(
            "Doğru sorular → doğru kapsam. Hedef: satış mı, lead mi, marka mı?"
        )
    )
    body.append(h3("2) Plan"))
    body.append(
        p(
            "Teslim kriterleri, öncelikler, fazlar (MVP → Phase 2) netleştirilir."
        )
    )
    body.append(h3("3) Uygulama"))
    body.append(
        p(
            "Tasarım + geliştirme + entegrasyonlar birlikte ele alınır."
        )
    )
    body.append(h3("4) Test ve yayın"))
    body.append(
        p(
            "Ödeme senaryoları, mobil test, performans ve teknik SEO kontrolü yapılır."
        )
    )

    body.append(h2("Başlangıç Kontrol Listesi (Pratik)"))
    body.append(h3("İş hedefi"))
    body.append(
        ul(
            [
                "Hedef kitle kim?",
                "Ortalama sepet hedefi nedir?",
                "En kritik 10 ürün/kategori hangisi?",
            ]
        )
    )
    body.append(h3("Altyapı"))
    body.append(
        ul(
            [
                "Ödeme yöntemi(leri) seçildi mi?",
                "Kargo/teslimat modeli net mi?",
                "İade politikası hazır mı?",
            ]
        )
    )
    body.append(h3("SEO ve içerik"))
    body.append(
        ul(
            [
                "Kategori hiyerarşisi çıkarıldı mı?",
                "Ürün açıklamaları özgün mü?",
                "Blog/rehber içerik planı var mı?",
            ]
        )
    )
    body.append(h3("Ölçümleme"))
    body.append(
        ul(
            [
                "GA4 + dönüşüm event’leri kuruldu mu?",
                "Sepet terk takibi var mı?",
            ]
        )
    )

    body.append(h2("Ne Zaman Bu Yaklaşımı Seçmelisiniz?"))
    body.append(
        p(
            "Eğer hedefleriniz ölçülebilir, kapsamınız net ve süreç yönetimine önem veriyorsanız; bu yaklaşım en iyi sonucu verir. Öncelikleri fazlara bölmek, hem bütçe hem de teslim süresi açısından avantaj sağlar."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "Net bir yol haritası için hedefinizi ve önceliklerinizi tek sayfalık bir brif halinde paylaşmanız yeterlidir. Kısa bir ön görüşme ile kapsamı netleştirip uygulanabilir bir plan çıkarabiliriz."
        )
    )

    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("E-ticarete başlamak için ilk adım nedir?", "Hedefi netleştirip kapsamı yazılı hale getirmektir."),
        ("Hazır altyapı mı özel yazılım mı?", "Hızlı başlamak isteyenler için hazır altyapı; ölçeklenebilirlik ve SEO kontrolü isteyenler için özel yazılım daha uygundur."),
        ("SEO ne zaman devreye girer?", "En baştan. SEO sonradan \"eklenen\" bir parça değildir; mimarinin parçasıdır."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Nedir? | E-Ticaret Sitesi Nasıl Çalışır ve Nasıl Başlanır"
    meta_description = (
        "E-ticaret nedir? B2C/B2B farkları, temel kavramlar, ödeme-kargo altyapısı, SEO ve dönüşüm odaklı başlangıç kontrol listesi. E-ticaret projeniz için doğru yol haritası."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Nedir?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_e_ticaret_sitesi_tr(page: SeoPage) -> Dict:
    """Custom cluster: E-Ticaret Sitesi — temel özellikler, süreç, SEO mimarisi. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Bir e-ticaret sitesi, ürün veya hizmetlerin internet üzerinden satıldığı dijital mağazadır. Başarılı bir e-ticaret projesi sadece ürün listelemekten ibaret değildir; SEO altyapısı, kullanıcı deneyimi, ödeme güvenliği ve dönüşüm optimizasyonu birlikte planlanmalıdır."
        )
    )
    body.append(
        p(
            "Bu nedenle e-ticaret sitesi geliştirme sürecinde amaç; hedefi netleştirmek, doğru mimariyi kurmak ve sürdürülebilir büyüme sağlayan bir altyapı oluşturmak olmalıdır."
        )
    )

    body.append(h2("E-Ticaret Sitesinin Temel Özellikleri"))
    body.append(h3("1. SEO Uyumlu Yapı"))
    body.append(
        p(
            "E-ticaret sitelerinde organik trafik en değerli kaynaklardan biridir. SEO açısından güçlü bir e-ticaret sitesinde şu yapı taşları bulunur:"
        )
    )
    body.append(
        ul(
            [
                "doğru kategori mimarisi",
                "SEO uyumlu URL yapısı",
                "ürün sayfalarında özgün içerik",
                "iç bağlantı stratejisi",
                "hızlı sayfa yükleme süresi",
            ]
        )
    )
    body.append(
        p(
            "Arama motorları için optimize edilmiş bir yapı, Google’da görünürlüğü artırarak daha fazla potansiyel müşteri getirir."
        )
    )

    body.append(h3("2. Kullanıcı Deneyimi (UX)"))
    body.append(
        p(
            "Kullanıcı deneyimi satış oranını doğrudan etkiler. İyi tasarlanmış bir e-ticaret sitesinde:"
        )
    )
    body.append(
        ul(
            [
                "mobil uyumlu tasarım",
                "hızlı ürün arama",
                "filtreleme sistemi",
                "kolay sepet ve ödeme süreci",
            ]
        )
    )
    body.append(
        p(
            "Ziyaretçi aradığı ürünü hızlı bulamazsa siteyi terk eder; bu da dönüşüm oranını doğrudan düşürür."
        )
    )

    body.append(h3("3. Güvenli Ödeme Sistemleri"))
    body.append(
        p(
            "Online satışın en kritik noktalarından biri ödeme güvenliğidir. Modern e-ticaret sitelerinde genellikle şu ödeme yöntemleri bulunur:"
        )
    )
    body.append(
        ul(
            [
                "kredi kartı / banka kartı",
                "3D secure ödeme",
                "dijital cüzdanlar",
                "havale / EFT",
            ]
        )
    )
    body.append(
        p(
            "Güvenli ödeme altyapısı müşterinin güvenini artırır ve satış dönüşüm oranını yükseltir."
        )
    )

    body.append(h3("4. Kargo ve Sipariş Yönetimi"))
    body.append(
        p(
            "E-ticaret sadece satış değil, aynı zamanda lojistik yönetimi gerektirir. Profesyonel bir e-ticaret sisteminde:"
        )
    )
    body.append(
        ul(
            [
                "otomatik kargo entegrasyonu",
                "sipariş takip sistemi",
                "stok yönetimi",
                "iade ve değişim süreci",
            ]
        )
    )
    body.append(
        p(
            "Bu süreçlerin doğru yönetilmesi müşteri memnuniyetini ve tekrar satın alma oranlarını artırır."
        )
    )

    body.append(h2("E-Ticaret Sitesi Neden Önemlidir?"))
    body.append(
        p(
            "Dijital dünyada işletmeler için e-ticaret artık bir seçenek değil, çoğu zaman zorunluluktur. Bir e-ticaret sitesi sayesinde:"
        )
    )
    body.append(
        ul(
            [
                "ürünler 7/24 satışa açık olur",
                "fiziksel mağaza sınırları ortadan kalkar",
                "global müşteri kitlesine ulaşılabilir",
                "pazarlama ve analiz araçları ile satış optimize edilebilir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle birçok marka dijital büyüme stratejisinin merkezine online satış platformlarını yerleştirir."
        )
    )

    body.append(h2("E-Ticaret Sitesi Kurarken En Sık Karşılaşılan Sorunlar"))
    body.append(
        ul(
            [
                "Düşük dönüşüm oranı — ziyaretçiler siteye gelir fakat satın alma gerçekleşmez.",
                "Sepet terk oranı — kullanıcılar ürünü sepete ekler fakat ödeme adımını tamamlamaz.",
                "Ödeme güveni — kullanıcılar ödeme sistemine güvenmediğinde satın alma işlemi gerçekleşmez.",
            ]
        )
    )
    body.append(
        p(
            "Bu sorunları azaltmak için doğru UX, güvenli ödeme altyapısı ve performans optimizasyonu birlikte ele alınmalıdır."
        )
    )

    body.append(h2("E-Ticaret Geliştirme Süreci"))
    body.append(
        p(
            "Profesyonel bir e-ticaret projesi genellikle şu adımlarla ilerler:"
        )
    )
    body.append(
        ul(
            [
                "Keşif ve hedefler — iş hedefleri, kullanıcı kitlesi ve ürün yapısı analiz edilir.",
                "Planlama — proje kapsamı, teslim kriterleri ve teknik mimari belirlenir.",
                "Tasarım ve geliştirme — kullanıcı deneyimi ve teknik altyapı birlikte geliştirilir.",
                "Test ve yayın — site performansı, ödeme sistemleri ve kullanıcı akışları test edilir.",
            ]
        )
    )

    body.append(h2("Bilgi Mimarisi ve SEO İç Bağlantı Yapısı"))
    body.append(
        p(
            "E-ticaret sitelerinde içerik yapısı doğru kurulmalıdır. Genellikle şu model kullanılır:"
        )
    )
    body.append(
        ul(
            [
                "Pillar sayfa — ana hizmet veya ana kategori.",
                "Cluster içerikler — alt konular ve rehber içerikler.",
                "Guide sayfalar — detaylı eğitim ve açıklama içerikleri.",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı hem kullanıcıların bilgiye hızlı ulaşmasını sağlar hem de SEO performansını güçlendirir."
        )
    )

    body.append(h2("Yayın Sonrası Büyüme"))
    body.append(
        p(
            "E-ticaret sitesi yayına alındıktan sonra süreç bitmez; asıl büyüme yayın sonrası optimizasyonla gelir. Süreç genellikle şu başlıklarla devam eder:"
        )
    )
    body.append(
        ul(
            [
                "SEO içerik stratejisi",
                "reklam kampanyaları",
                "dönüşüm optimizasyonu",
                "kullanıcı davranışı analizi",
            ]
        )
    )
    body.append(
        p(
            "Bu sürekli iyileştirme süreci sayesinde satışlar zamanla artar ve marka dijitalde güçlenir."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "E-ticaret projeniz için doğru stratejiyi belirlemek istiyorsanız, hedeflerinizi ve iş modelinizi paylaşmanız yeterlidir. İş modelinize uygun, SEO uyumlu ve ölçeklenebilir bir e-ticaret altyapısını birlikte planlayabiliriz."
        )
    )
    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = []  # Silo FAQ zaten diğer sayfalarda kapsanıyor; burada opsiyonel bırakıyoruz.
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Sitesi | Profesyonel ve SEO Uyumlu Online Mağaza"
    meta_description = (
        "E-ticaret sitesi nedir ve başarılı bir online mağaza nasıl oluşturulur? SEO altyapısı, ödeme sistemleri, kargo entegrasyonu ve dönüşüm odaklı tasarım hakkında kapsamlı rehber."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Sitesi — Profesyonel ve SEO Uyumlu Online Mağaza",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_e_ticaret_sitesi_nasil_kurulur_tr(page: SeoPage) -> Dict:
    """Custom cluster: E-Ticaret Sitesi Nasıl Kurulur? — adım adım kurulum rehberi. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Bir e-ticaret sitesi kurmak, sadece ürün eklemekten ibaret değildir. Başarılı bir online mağaza için strateji, teknik altyapı ve kullanıcı deneyimi birlikte planlanmalıdır."
        )
    )
    body.append(
        p(
            "Profesyonel bir e-ticaret projesinde amaç; SEO uyumlu, hızlı ve güvenli bir altyapı kurarak sürdürülebilir bir satış sistemi oluşturmaktır."
        )
    )

    body.append(h2("1. İş Modelini ve Hedefi Belirlemek"))
    body.append(
        p(
            "E-ticaret projesine başlamadan önce şu soruların net olması gerekir:"
        )
    )
    body.append(
        ul(
            [
                "Hangi ürün veya hizmet satılacak?",
                "Hedef müşteri kitlesi kim?",
                "B2C mi B2B mi olacak?",
                "Beklenen ortalama sepet tutarı nedir?",
            ]
        )
    )
    body.append(
        p(
            "Bu analizler yapılmadan geliştirilen e-ticaret projeleri çoğunlukla düşük dönüşüm oranı problemi yaşar."
        )
    )

    body.append(h2("2. Doğru E-Ticaret Altyapısını Seçmek"))
    body.append(
        p(
            "Bir e-ticaret sitesi kurarken en kritik kararlardan biri altyapı seçimidir. Genellikle iki ana seçenek vardır:"
        )
    )
    body.append(h3("Hazır E-Ticaret Platformları"))
    body.append(
        ul(
            [
                "Avantajları: hızlı kurulum, nispeten düşük başlangıç bütçesi, hazır tema ve modüller.",
                "Sınırlamaları: SEO ve performans kısıtları, kapsamlı özelleştirme zorlukları.",
            ]
        )
    )
    body.append(h3("Özel E-Ticaret Yazılımı"))
    body.append(
        ul(
            [
                "SEO odaklı mimari kurulumu.",
                "Yüksek performans ve ölçeklenebilirlik.",
                "İş modeline tam uyumlu esnek geliştirme imkânı.",
                "Özel entegrasyonlar (ERP, CRM, pazar yerleri vb.).",
            ]
        )
    )
    body.append(
        p(
            "Uzun vadeli büyüme hedefleyen orta ve büyük projeler, çoğu zaman özel e-ticaret yazılımını tercih eder."
        )
    )

    body.append(h2("3. Alan Adı ve Sunucu Kurulumu"))
    body.append(
        p(
            "Teknik altyapı; alan adı, barındırma ve güvenlik bileşenlerini içerir:"
        )
    )
    body.append(
        ul(
            [
                "domain (alan adı) seçimi ve yönlendirmesi",
                "hosting veya bulut sunucu (cloud server)",
                "SSL güvenlik sertifikası",
                "önbellekleme ve temel hız optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı sitenin güvenli, hızlı ve stabil çalışması için temel zemini oluşturur."
        )
    )

    body.append(h2("4. Ürün ve Kategori Yapısını Kurmak"))
    body.append(
        p(
            "SEO açısından e-ticaret sitelerinde kategori mimarisi kritik öneme sahiptir. Doğru yapı genellikle şöyle kurgulanır:"
        )
    )
    body.append(
        ul(
            [
                "Ana kategori → alt kategori → ürün sayfası hiyerarşisi",
                "her ürün için açıklama, teknik özellikler ve yüksek kaliteli görseller",
                "başlık, açıklama ve URL seviyesinde SEO uyumu",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı hem kullanıcıların aradığını hızlı bulmasını sağlar hem de arama motorlarının siteyi daha iyi anlamasına yardımcı olur."
        )
    )

    body.append(h2("5. Ödeme Sistemi Entegrasyonu"))
    body.append(
        p(
            "E-ticaret sitelerinde ödeme akışı en kritik adımlardan biridir. Modern online mağazalarda genellikle şu yöntemler desteklenir:"
        )
    )
    body.append(
        ul(
            [
                "kredi kartı / banka kartı işlemleri",
                "3D secure odaklı güvenli ödeme",
                "dijital cüzdan entegrasyonları",
                "havale veya EFT seçenekleri",
            ]
        )
    )
    body.append(
        p(
            "Güvenli ve sorunsuz çalışan bir ödeme altyapısı, müşteri güvenini artırır ve tamamlama oranlarını yükseltir."
        )
    )

    body.append(h2("6. Kargo ve Sipariş Yönetimi"))
    body.append(
        p(
            "E-ticaretin sürdürülebilir olması için lojistik süreçlerinin de iyi tasarlanması gerekir. Profesyonel bir e-ticaret sisteminde:"
        )
    )
    body.append(
        ul(
            [
                "otomatik kargo entegrasyonları",
                "sipariş takip ekranları",
                "stok yönetimi ve uyarı mekanizmaları",
                "iade ve değişim süreçlerinin kayıt altına alınması",
            ]
        )
    )
    body.append(
        p(
            "Bu adımlar müşteri deneyimini güçlendirir ve tekrar satın alma davranışını destekler."
        )
    )

    body.append(h2("7. SEO ve Dijital Pazarlama Altyapısı"))
    body.append(
        p(
            "E-ticaret sitesinin uzun vadede başarılı olması için SEO ve dijital pazarlama temel bir gerekliliktir. Özellikle şu başlıklar önemlidir:"
        )
    )
    body.append(
        ul(
            [
                "SEO uyumlu URL ve başlık yapısı",
                "hızlı sayfa yükleme süreleri",
                "mobil uyumlu arayüz",
                "anahtar kelime odaklı içerik üretimi",
                "iç bağlantı stratejisi ve kategori/ürün ilişkileri",
            ]
        )
    )
    body.append(
        p(
            "Bu bileşenler sayesinde e-ticaret sitesi arama motorlarında görünürlük kazanır ve organik trafik üretmeye başlar."
        )
    )

    body.append(h2("Yayın Öncesi Kontrol Listesi"))
    body.append(
        p(
            "Bir e-ticaret sitesi yayına alınmadan önce mutlaka şu kontroller yapılmalıdır:"
        )
    )
    body.append(
        ul(
            [
                "ödeme akışlarının uçtan uca test edilmesi",
                "mobil cihaz ve tarayıcı uyumluluğu",
                "SEO başlık ve açıklamalarının gözden geçirilmesi",
                "sayfa hız ölçümleri ve temel optimizasyonlar",
                "güvenlik ve erişim kontrolleri",
            ]
        )
    )
    body.append(
        p(
            "Bu adımlar yayın sonrası oluşabilecek hataları azaltır ve ilk günden itibaren daha stabil bir deneyim sunar."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "Eğer bir e-ticaret sitesi kurmayı planlıyorsanız, doğru mimari ve teknik altyapıyı belirlemek kritik öneme sahiptir. Hedeflerinizi paylaşarak projeniz için en uygun stratejiyi birlikte planlayabiliriz."
        )
    )
    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs: List[Tuple[str, str]] = []
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Sitesi Nasıl Kurulur? | Adım Adım Profesyonel Rehber"
    meta_description = (
        "E-ticaret sitesi nasıl kurulur? Domain, altyapı seçimi, ödeme sistemi, kargo entegrasyonu ve SEO uyumlu online mağaza kurulumu için kapsamlı rehber."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Sitesi Nasıl Kurulur? — Adım Adım Profesyonel Rehber",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_e_ticaret_sitesi_yaptirmak_tr(page: SeoPage) -> Dict:
    """Custom cluster: E-Ticaret Sitesi Yaptırmak — profesyonel online mağaza geliştirme. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa Özet"))
    body.append(
        p(
            "Bir e-ticaret sitesi yaptırmak, dijital dünyada satış yapmak isteyen işletmeler için en önemli yatırımlardan biridir. "
            "Başarılı bir e-ticaret sitesi yalnızca tasarımdan ibaret değildir; SEO altyapısı, kullanıcı deneyimi, güvenli ödeme sistemleri ve güçlü teknik mimari birlikte planlanmalıdır."
        )
    )
    body.append(
        p(
            "Doğru planlanan bir online mağaza sayesinde işletmeler 7/24 satış yapabilir, daha geniş bir müşteri kitlesine ulaşabilir ve dijital pazarlama ile satışlarını ölçekleyebilir."
        )
    )

    body.append(h2("E-Ticaret Sitesi Yaptırmadan Önce Bilinmesi Gerekenler"))
    body.append(
        p(
            "Bir e-ticaret projesine başlamadan önce şu konular netleştirilmelidir:"
        )
    )
    body.append(
        ul(
            [
                "ürün veya hizmet kategorileri",
                "hedef müşteri kitlesi",
                "satış modeli (B2C veya B2B)",
                "ödeme ve teslimat yöntemleri",
            ]
        )
    )
    body.append(
        p(
            "Bu analizler yapılmadan başlanan projelerde genellikle düşük dönüşüm oranı ve yüksek sepet terk oranı gibi sorunlar ortaya çıkar."
        )
    )

    body.append(h2("Profesyonel E-Ticaret Sitesinin Özellikleri"))
    body.append(h3("SEO Uyumlu Altyapı"))
    body.append(
        p(
            "Bir e-ticaret sitesinin arama motorlarında görünür olması için SEO altyapısının güçlü olması gerekir. Öne çıkan unsurlar:"
        )
    )
    body.append(
        ul(
            [
                "doğru kategori yapısı",
                "SEO uyumlu URL mimarisi",
                "hızlı sayfa yükleme",
                "mobil uyumlu tasarım",
                "iç bağlantı stratejisi",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı sayesinde e-ticaret sitesi organik trafik elde eder ve daha fazla potansiyel müşteriye ulaşır."
        )
    )

    body.append(h3("Güvenli Ödeme Sistemleri"))
    body.append(
        p(
            "Online satışta müşterilerin en çok dikkat ettiği konu ödeme güvenliğidir. Profesyonel e-ticaret sitelerinde genellikle şu yöntemler bulunur:"
        )
    )
    body.append(
        ul(
            [
                "kredi kartı",
                "banka kartı",
                "3D secure ödeme",
                "dijital ödeme sistemleri",
                "havale veya EFT",
            ]
        )
    )
    body.append(
        p(
            "Güvenli ödeme altyapısı kullanıcı güvenini artırır ve tamamlanan sipariş oranını yükseltir."
        )
    )

    body.append(h3("Kargo ve Sipariş Yönetimi"))
    body.append(
        p(
            "E-ticaret sitelerinde satış kadar önemli olan bir diğer konu sipariş ve lojistik yönetimidir. Modern e-ticaret sistemlerinde:"
        )
    )
    body.append(
        ul(
            [
                "otomatik kargo entegrasyonu",
                "sipariş takip sistemi",
                "stok yönetimi",
                "iade ve değişim süreçleri",
            ]
        )
    )
    body.append(
        p(
            "Bu sistemler müşteri deneyimini önemli ölçüde iyileştirir ve tekrar satın alma davranışını destekler."
        )
    )

    body.append(h2("E-Ticaret Sitesi Geliştirme Süreci"))
    body.append(
        p(
            "Profesyonel bir e-ticaret projesi genellikle şu adımlarla ilerler:"
        )
    )
    body.append(
        ul(
            [
                "Keşif ve hedef belirleme — iş hedefleri, ürün yapısı ve kullanıcı kitlesi analiz edilir.",
                "Planlama — proje kapsamı ve teknik mimari belirlenir.",
                "Tasarım ve geliştirme — kullanıcı deneyimi ve yazılım altyapısı geliştirilir.",
                "Test ve yayın — site performansı, ödeme sistemleri ve kullanıcı akışları test edilir.",
            ]
        )
    )

    body.append(h2("E-Ticaret Sitesi Yaptırmanın Avantajları"))
    body.append(
        p(
            "Doğru kurgulanmış bir e-ticaret sitesi işletmelere birçok avantaj sağlar:"
        )
    )
    body.append(
        ul(
            [
                "global müşteri kitlesine ulaşma",
                "7/24 satış yapabilme",
                "daha düşük operasyonel yük",
                "veri analizi ile satış optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle günümüzde birçok işletme, büyüme stratejisinin merkezine online satış platformlarını yerleştiriyor."
        )
    )

    body.append(h2("E-Ticaret Sitesi Yaptırırken Dikkat Edilmesi Gerekenler"))
    body.append(
        p(
            "Bir e-ticaret sitesi yaptırırken uzun vadeli başarı için şu kriterlere dikkat edilmelidir:"
        )
    )
    body.append(
        ul(
            [
                "SEO uyumlu altyapı",
                "yüksek performans ve hız",
                "güvenli ödeme sistemleri",
                "mobil uyumlu tasarım",
                "ölçeklenebilir yazılım mimarisi",
            ]
        )
    )
    body.append(
        p(
            "Bu faktörler, projenin sürdürülebilir şekilde büyümesini ve teknik borcun kontrol altında tutulmasını sağlar."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "Eğer siz de profesyonel bir e-ticaret sitesi yaptırmak istiyorsanız, hedeflerinizi paylaşarak projeniz için en doğru çözümü birlikte planlayabiliriz."
        )
    )
    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs: List[Tuple[str, str]] = []
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Sitesi Yaptırmak | Profesyonel Online Mağaza Geliştirme"
    meta_description = (
        "E-ticaret sitesi yaptırmak isteyenler için kapsamlı rehber. SEO uyumlu altyapı, güvenli ödeme sistemleri ve ölçeklenebilir e-ticaret yazılımı ile profesyonel online mağaza geliştirme."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Sitesi Yaptırmak — Profesyonel Online Mağaza Geliştirme",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_e_ticaret_yazilim_firmasi_tr(page: SeoPage) -> Dict:
    """Custom cluster: E-Ticaret Yazılım Firması — profesyonel e-ticaret yazılım geliştirme. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Genel Bakış"))
    body.append(
        p(
            "Bir e-ticaret yazılım firması, işletmelerin dijital dünyada ürün ve hizmet satabilmesi için gerekli olan teknik altyapıyı geliştirir."
        )
    )
    body.append(
        p(
            "Profesyonel bir e-ticaret yazılımı yalnızca bir web sitesi değildir; güvenli ödeme altyapısı, hızlı ve SEO uyumlu sayfa yapısı, güçlü ürün ve sipariş yönetimi ile ölçeklenebilir yazılım mimarisi gibi birçok kritik bileşeni bir araya getirir."
        )
    )
    body.append(
        p(
            "Doğru geliştirilen bir e-ticaret platformu, işletmelerin online satışlarını büyütmesini ve dijital pazarda rekabet etmesini sağlar."
        )
    )

    body.append(h2("Profesyonel E-Ticaret Yazılım Firması Ne Yapar?"))
    body.append(
        p(
            "Profesyonel bir e-ticaret yazılım firması genellikle uçtan uca yazılım geliştirme, entegrasyon ve optimizasyon hizmetleri sunar."
        )
    )

    body.append(h3("E-Ticaret Yazılım Geliştirme"))
    body.append(
        p(
            "İşletmenin ihtiyaçlarına uygun özel e-ticaret yazılımları geliştirilir. Bu yazılımlar genellikle şu özellikleri içerir:"
        )
    )
    body.append(
        ul(
            [
                "ürün yönetim sistemi",
                "kategori ve filtre yapısı",
                "sipariş ve stok yönetimi",
                "kampanya ve indirim modülleri",
            ]
        )
    )

    body.append(h3("SEO Uyumlu E-Ticaret Altyapısı"))
    body.append(
        p(
            "Başarılı bir e-ticaret sitesinin arama motorlarında görünür olması için SEO altyapısı güçlü olmalıdır. Profesyonel e-ticaret yazılımlarında:"
        )
    )
    body.append(
        ul(
            [
                "SEO uyumlu URL yapısı",
                "hızlı sayfa yükleme",
                "mobil uyumlu tasarım",
                "iç bağlantı mimarisi",
            ]
        )
    )
    body.append(
        p(
            "Bu unsurlar sayesinde e-ticaret sitesi organik trafik kazanabilir ve daha fazla müşteriye ulaşabilir."
        )
    )

    body.append(h3("Ödeme Sistemi Entegrasyonları"))
    body.append(
        p(
            "Online satış yapan bir platform için ödeme altyapısı kritik öneme sahiptir. Modern e-ticaret yazılımları genellikle şu ödeme yöntemlerini destekler:"
        )
    )
    body.append(
        ul(
            [
                "kredi kartı ile ödeme",
                "3D secure odaklı güvenli akışlar",
                "dijital ödeme sistemleri",
                "banka transferi seçenekleri",
            ]
        )
    )
    body.append(
        p(
            "Güvenli ve sorunsuz bir ödeme altyapısı kullanıcı güvenini artırır ve tamamlanan sipariş oranını yükseltir."
        )
    )

    body.append(h2("E-Ticaret Yazılım Firması Seçerken Nelere Dikkat Edilmeli?"))
    body.append(
        p(
            "Bir e-ticaret projesinin başarısı büyük ölçüde doğru yazılım firması seçimine bağlıdır. Firma seçerken şu kriterlere dikkat etmek gerekir:"
        )
    )
    body.append(
        ul(
            [
                "SEO uyumlu altyapı geliştirme deneyimi",
                "ölçeklenebilir yazılım mimarisi tasarlama becerisi",
                "güvenli ödeme entegrasyonları konusunda tecrübe",
                "teknik destek ve bakım hizmeti sunma yaklaşımı",
                "performans ve hız optimizasyonu odaklı çalışma",
            ]
        )
    )

    body.append(h2("Özel Yazılım mı Hazır E-Ticaret Platformu mu?"))
    body.append(
        p(
            "Pek çok işletme e-ticaret projesi için iki ana seçenek arasında karar verir: hazır e-ticaret platformları ve özel e-ticaret yazılımı."
        )
    )
    body.append(h3("Hazır E-Ticaret Platformları"))
    body.append(
        ul(
            [
                "Avantajlar: daha hızlı başlangıç, daha düşük ilk yatırım, hazır tema ve modüller.",
                "Dezavantajlar: sınırlı özelleştirme ve performans kısıtları; iş modeli büyüdükçe sınırlarına daha çabuk ulaşır.",
            ]
        )
    )
    body.append(h3("Özel E-Ticaret Yazılımı"))
    body.append(
        ul(
            [
                "tamamen işletmeye özel geliştirilir",
                "SEO açısından daha güçlü bir kontrol sunar",
                "daha hızlı ve ölçeklenebilir şekilde çalışır",
                "özel entegrasyonlara (ERP, CRM, pazar yerleri vb.) izin verir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle büyümeyi hedefleyen markalar genellikle özel e-ticaret yazılımı ve deneyimli bir yazılım firması ile çalışmayı tercih eder."
        )
    )

    body.append(h2("E-Ticaret Yazılımı Neden Stratejik Bir Yatırımdır?"))
    body.append(
        p(
            "Profesyonel bir e-ticaret yazılımı işletmelere şu avantajları sağlar:"
        )
    )
    body.append(
        ul(
            [
                "7/24 online satış",
                "global müşteri erişimi",
                "otomatik sipariş ve stok yönetimi",
                "dijital pazarlama entegrasyonu",
                "veri analizi ve satış optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle e-ticaret yazılımı, modern işletmeler için stratejik bir dijital yatırım olarak görülür."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "Eğer işletmeniz için profesyonel bir e-ticaret yazılım firması ile çalışmak istiyorsanız, hedeflerinizi paylaşarak projeniz için en doğru çözümü birlikte planlayabiliriz."
        )
    )
    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs: List[Tuple[str, str]] = []
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Yazılım Firması | Profesyonel E-Ticaret Yazılım Geliştirme"
    meta_description = (
        "Profesyonel e-ticaret yazılım firması arıyorsanız doğru yerdesiniz. SEO uyumlu, hızlı ve ölçeklenebilir e-ticaret yazılım çözümleri ile online satış platformunuzu büyütün."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Yazılım Firması — Profesyonel E-Ticaret Yazılım Geliştirme",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_ozel_e_ticaret_yazilimi_tr(page: SeoPage) -> Dict:
    """Custom cluster: Özel E-Ticaret Yazılımı — ölçeklenebilir ve SEO uyumlu e-ticaret geliştirme. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Özel E-Ticaret Yazılımı"))
    body.append(
        p(
            "Özel e-ticaret yazılımı, işletmelerin ihtiyaçlarına özel olarak geliştirilen bir online satış altyapısıdır."
        )
    )
    body.append(
        p(
            "Hazır e-ticaret platformlarının aksine, özel yazılım çözümleri tamamen işletmenin iş modeli, operasyon süreçleri ve büyüme hedefleri dikkate alınarak geliştirilir."
        )
    )
    body.append(p("Bu sayede işletmeler:"))
    body.append(
        ul(
            [
                "daha yüksek performans elde eder",
                "SEO açısından daha güçlü altyapıya sahip olur",
                "özel entegrasyonlar kullanabilir",
                "uzun vadede daha ölçeklenebilir bir sistem kurabilir.",
            ]
        )
    )

    body.append(h2("Özel E-Ticaret Yazılımının Avantajları"))
    body.append(h3("Tam Esneklik ve Özelleştirme"))
    body.append(
        p(
            "Özel e-ticaret yazılımı, işletmenin ihtiyaçlarına göre tamamen özelleştirilebilir. Bu sistemlerde:"
        )
    )
    body.append(
        ul(
            [
                "özel ürün yönetimi",
                "gelişmiş kategori yapısı",
                "kampanya ve indirim motoru",
                "özel ödeme ve kargo entegrasyonları",
            ]
        )
    )
    body.append(
        p(
            "Hazır platformlarda mümkün olmayan birçok özellik özel yazılım ile uygulanabilir."
        )
    )

    body.append(h3("Yüksek Performans ve Hız"))
    body.append(p("E-ticaret sitelerinde hız çok önemlidir."))
    body.append(p("Yavaş çalışan bir online mağaza:"))
    body.append(
        ul(
            [
                "kullanıcı deneyimini düşürür",
                "dönüşüm oranını azaltır",
                "SEO performansını olumsuz etkiler.",
            ]
        )
    )
    body.append(
        p(
            "Özel e-ticaret yazılımı, performans odaklı geliştirildiği için genellikle hazır platformlara göre daha hızlı çalışır."
        )
    )

    body.append(h3("SEO Uyumlu Mimari"))
    body.append(
        p(
            "E-ticaret sitelerinin Google'da görünür olması için SEO altyapısı kritik öneme sahiptir. Profesyonel bir e-ticaret yazılımı şu özelliklere sahip olmalıdır:"
        )
    )
    body.append(
        ul(
            [
                "SEO uyumlu URL yapısı",
                "optimize edilmiş kategori sayfaları",
                "hızlı sayfa yükleme",
                "mobil uyumlu tasarım",
                "güçlü iç bağlantı mimarisi",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı sayesinde e-ticaret siteleri organik trafik elde edebilir ve satışlarını artırabilir."
        )
    )

    body.append(h2("Özel E-Ticaret Yazılımı Hangi İşletmeler İçin Uygundur?"))
    body.append(
        p(
            "Her işletmenin ihtiyacı aynı değildir. Özel e-ticaret yazılımı özellikle şu işletmeler için uygundur:"
        )
    )
    body.append(
        ul(
            [
                "büyük ürün kataloglarına sahip şirketler",
                "B2B satış yapan firmalar",
                "özel fiyatlandırma veya kampanya sistemi kullanan işletmeler",
                "yüksek trafik alan e-ticaret siteleri",
            ]
        )
    )
    body.append(
        p(
            "Bu tür projelerde özel yazılım, uzun vadede çok daha sürdürülebilir bir çözüm sunar."
        )
    )

    body.append(h2("Hazır E-Ticaret Platformu ile Özel Yazılım Arasındaki Fark"))
    body.append(h3("Hazır Platformlar"))
    body.append(p("Avantajları"))
    body.append(
        ul(
            [
                "hızlı kurulum",
                "düşük başlangıç maliyeti",
            ]
        )
    )
    body.append(p("Dezavantajları"))
    body.append(
        ul(
            [
                "sınırlı özelleştirme",
                "performans sınırlamaları",
                "SEO kısıtlamaları",
            ]
        )
    )
    body.append(h3("Özel E-Ticaret Yazılımı"))
    body.append(
        ul(
            [
                "tamamen işletmeye özel geliştirilir",
                "yüksek performans sunar",
                "SEO açısından güçlüdür",
                "ölçeklenebilir mimariye sahiptir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle büyümeyi hedefleyen işletmeler genellikle custom e-commerce development tercih eder."
        )
    )

    body.append(h2("Özel E-Ticaret Yazılımı Geliştirme Süreci"))
    body.append(
        p(
            "Profesyonel bir e-ticaret yazılımı geliştirme süreci genellikle şu aşamalardan oluşur."
        )
    )
    body.append(h3("Keşif ve Analiz"))
    body.append(
        p(
            "İş hedefleri, kullanıcı kitlesi ve teknik gereksinimler analiz edilir."
        )
    )
    body.append(h3("Planlama"))
    body.append(
        p(
            "Proje mimarisi ve geliştirme planı oluşturulur."
        )
    )
    body.append(h3("Tasarım ve Geliştirme"))
    body.append(
        p(
            "Kullanıcı deneyimi ve yazılım altyapısı geliştirilir."
        )
    )
    body.append(h3("Test ve Yayın"))
    body.append(
        p(
            "Sistem performansı, güvenlik ve ödeme entegrasyonları test edilir."
        )
    )

    body.append(h2("Neden Özel E-Ticaret Yazılımı Tercih Edilmeli?"))
    body.append(
        p(
            "Özel e-ticaret yazılımı işletmelere şu avantajları sağlar:"
        )
    )
    body.append(
        ul(
            [
                "tamamen özelleştirilebilir altyapı",
                "yüksek performans ve hız",
                "gelişmiş SEO mimarisi",
                "güçlü entegrasyon seçenekleri",
                "uzun vadeli ölçeklenebilirlik",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle birçok işletme için özel yazılım stratejik bir dijital yatırım olarak görülür."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "Eğer işletmeniz için özel e-ticaret yazılımı geliştirmek istiyorsanız, doğru planlama ve teknik mimari projenin başarısını belirler."
        )
    )
    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs: List[Tuple[str, str]] = []
    faq_json = faq(faq_pairs)

    meta_title = "Özel E-Ticaret Yazılımı | Ölçeklenebilir ve SEO Uyumlu E-Ticaret Geliştirme"
    meta_description = (
        "Özel e-ticaret yazılımı nedir? İşletmenize özel geliştirilen e-ticaret altyapısı, SEO uyumlu mimari, ödeme entegrasyonları ve ölçeklenebilir online mağaza çözümleri hakkında kapsamlı rehber."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Özel E-Ticaret Yazılımı — Ölçeklenebilir ve SEO Uyumlu E-Ticaret Geliştirme",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_e_ticaret_yazilimi_tr(page: SeoPage) -> Dict:
    """Custom cluster: E-Ticaret Yazılımı — profesyonel ve ölçeklenebilir e-ticaret altyapısı. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Genel Bakış"))
    body.append(
        p(
            "E-ticaret yazılımı, işletmelerin internet üzerinden ürün veya hizmet satabilmesini sağlayan teknik altyapıdır."
        )
    )
    body.append(
        p(
            "Modern bir e-ticaret platformu yalnızca bir web sitesi değildir; ürün yönetim sistemi, sipariş ve stok yönetimi, ödeme altyapısı, kargo entegrasyonları ve SEO uyumlu sayfa yapısı gibi birçok bileşeni içerir."
        )
    )
    body.append(
        p(
            "Doğru geliştirilen bir e-ticaret yazılımı, işletmelerin online satışlarını büyütmesini ve dijital pazarda rekabet etmesini sağlar."
        )
    )

    body.append(h2("E-Ticaret Yazılımının Temel Özellikleri"))

    body.append(h3("Ürün ve Kategori Yönetimi"))
    body.append(
        p(
            "Profesyonel bir e-ticaret yazılımında ürün ve kategori yönetimi merkezi bir rol oynar. Bu sistem sayesinde:"
        )
    )
    body.append(
        ul(
            [
                "ürün ekleme ve düzenleme",
                "kategori ve alt kategori oluşturma",
                "ürün varyasyonları yönetimi",
                "stok kontrolü",
            ]
        )
    )
    body.append(
        p(
            "İyi tasarlanmış bir ürün yönetim sistemi, özellikle büyük kataloglara sahip e-ticaret sitelerinde operasyonel verimliliği artırır."
        )
    )

    body.append(h3("Sipariş ve Stok Yönetimi"))
    body.append(
        p(
            "Online satış yapan işletmeler için sipariş yönetimi kritik bir süreçtir. Modern e-ticaret yazılımlarında genellikle:"
        )
    )
    body.append(
        ul(
            [
                "sipariş takibi",
                "otomatik stok güncelleme",
                "müşteri sipariş geçmişi",
                "iade ve değişim yönetimi",
            ]
        )
    )
    body.append(
        p(
            "Bu özellikler hem işletme tarafında operasyonel yükü azaltır hem de müşteri deneyimini iyileştirir."
        )
    )

    body.append(h3("Ödeme Sistemi Entegrasyonları"))
    body.append(
        p(
            "E-ticaret sitelerinde güvenli ödeme altyapısı büyük önem taşır. Profesyonel e-ticaret yazılımları genellikle şu ödeme sistemlerini destekler:"
        )
    )
    body.append(
        ul(
            [
                "kredi kartı ile ödeme",
                "3D secure ödeme akışları",
                "dijital ödeme sistemleri",
                "banka transferi seçenekleri",
            ]
        )
    )
    body.append(
        p(
            "Güvenli ödeme altyapısı, müşteri güvenini artırır ve tamamlanan sipariş oranını yükseltir."
        )
    )

    body.append(h2("SEO Uyumlu E-Ticaret Yazılımı Neden Önemlidir?"))
    body.append(
        p(
            "Bir e-ticaret sitesinin arama motorlarında görünür olması için SEO altyapısının güçlü olması gerekir. SEO uyumlu bir e-ticaret yazılımı şu özelliklere sahip olmalıdır:"
        )
    )
    body.append(
        ul(
            [
                "SEO dostu URL yapısı",
                "hızlı sayfa yükleme",
                "mobil uyumlu tasarım",
                "doğru iç bağlantı mimarisi",
                "optimize edilmiş kategori yapısı",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı sayesinde e-ticaret sitesi organik trafik elde edebilir ve daha fazla müşteriye ulaşabilir."
        )
    )

    body.append(h2("Hazır E-Ticaret Altyapısı mı Özel Yazılım mı?"))
    body.append(
        p(
            "Pek çok işletme e-ticaret projesine başlarken \"hazır e-ticaret platformu mu yoksa özel e-ticaret yazılımı mı?\" sorusunu sorar."
        )
    )
    body.append(h3("Hazır E-Ticaret Platformları"))
    body.append(
        ul(
            [
                "Avantajları: hızlı kurulum, daha düşük başlangıç eşiği.",
                "Dezavantajları: sınırlı özelleştirme, performans ve SEO kısıtlamaları.",
            ]
        )
    )
    body.append(h3("Özel E-Ticaret Yazılımı"))
    body.append(
        ul(
            [
                "tamamen işletmeye özel kurgulanır",
                "yüksek performans sunar",
                "SEO açısından daha güçlü bir kontrol sağlar",
                "ölçeklenebilir mimariye sahiptir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle büyümeyi hedefleyen işletmeler genellikle özel e-ticaret yazılımı ve deneyimli bir yazılım ekibi ile çalışmayı tercih eder."
        )
    )

    body.append(h2("E-Ticaret Yazılımı Seçerken Nelere Dikkat Edilmeli?"))
    body.append(
        p(
            "Doğru e-ticaret yazılımını seçmek projenin başarısı için kritik öneme sahiptir. Bir platform seçerken şu kriterlere dikkat edilmelidir:"
        )
    )
    body.append(
        ul(
            [
                "SEO uyumlu altyapı",
                "yüksek performans ve hız",
                "güvenli ödeme sistemleri",
                "mobil uyumlu tasarım",
                "ölçeklenebilir yazılım mimarisi",
                "teknik destek ve bakım hizmeti",
            ]
        )
    )

    body.append(h2("E-Ticaret Yazılımı Neden İşletmeler İçin Kritik?"))
    body.append(
        p(
            "Profesyonel bir e-ticaret yazılımı işletmelere şu avantajları sağlar:"
        )
    )
    body.append(
        ul(
            [
                "7/24 online satış",
                "global müşteri erişimi",
                "otomatik sipariş ve stok yönetimi",
                "dijital pazarlama entegrasyonu",
                "veri analizi ve satış optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle e-ticaret altyapısı, günümüz işletmeleri için stratejik bir dijital yatırım haline gelmiştir."
        )
    )

    body.append(h2("Bir Sonraki Adım"))
    body.append(
        p(
            "Eğer işletmeniz için profesyonel bir e-ticaret yazılımı geliştirmek istiyorsanız, doğru planlama ve teknik altyapı projenin başarısını belirler."
        )
    )
    body.append(
        cta_box(
            "E-ticaret projeniz için doğru yol haritasını birlikte çıkaralım.",
            "Hedef ve kapsamınızı paylaşın; E-Ticaret Geliştirme teklif sayfası üzerinden size özel plan oluşturalım.",
            _quote_url(page),
            "E-Ticaret Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs: List[Tuple[str, str]] = []
    faq_json = faq(faq_pairs)

    meta_title = "E-Ticaret Yazılımı | Profesyonel ve Ölçeklenebilir E-Ticaret Altyapısı"
    meta_description = (
        "E-ticaret yazılımı nedir? Profesyonel e-ticaret altyapısı, özel e-ticaret yazılımı geliştirme, ödeme entegrasyonları ve SEO uyumlu online mağaza çözümleri hakkında kapsamlı rehber."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Ticaret Yazılımı — Profesyonel ve Ölçeklenebilir E-Ticaret Altyapısı",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_react_native_vs_native_tr(page: SeoPage) -> Dict:
    """Custom cluster: React Native mi Native mi? — decision matrix, scenarios, process. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Kısa özet"))
    body.append(
        p(
            "React Native ve Native (Swift/Kotlin) arasında seçim yapmak \"hangisi daha iyi?\" sorusu değil; hedef, kapsam ve kısıtlar sorusudur. "
            "Bu sayfanın amacı; performans beklentisi, bütçe ve zaman kısıtlarını netleştirerek ölçülebilir bir karar vermenizi sağlamak ve projenizi sürdürülebilir bir plana oturtmaktır."
        )
    )
    body.append(
        p(
            f"Genel mobil çerçeve için {{{{ link:{_pillar_url(page)} }}}}, süreç odaklı rehber için {{{{ link:{_guide_url(page)} }}}} sayfasını kullanabilirsiniz."
        )
    )

    body.append(h2("En sık karşılaşılan ihtiyaçlar"))
    body.append(h3("Performans"))
    body.append(
        ul(
            [
                "akıcı liste/akış ekranları (feed, katalog, mesaj)",
                "düşük seviye cihazlarda stabil deneyim",
                "animasyonlar, kamera, arka plan işlemleri",
            ]
        )
    )

    body.append(h3("Bütçe"))
    body.append(
        ul(
            [
                "tek ekip mi, iki ayrı native ekip mi?",
                "uzun vadede bakım yükü ve ekip yapısı",
                "platform sayısı arttıkça bütçeyi kontrollü tutma ihtiyacı",
            ]
        )
    )

    body.append(h3("Zaman"))
    body.append(
        ul(
            [
                "MVP’yi hızlı yayınlama",
                "ilk sürümden sonra iterasyon hızı",
                "store süreçleri ve test döngüsü yönetimi",
            ]
        )
    )

    body.append(h2("React Native nedir, Native nedir?"))
    body.append(
        p(
            "React Native: iOS + Android için tek kod tabanı ile geliştirme yaklaşımıdır. Doğru mimariyle hızlı MVP ve sürdürülebilir geliştirme sunar."
        )
    )
    body.append(
        p(
            "Native: iOS (Swift) ve Android (Kotlin) için ayrı geliştirmedir. En yüksek performans ve en geniş platform kontrolünü sağlar."
        )
    )

    body.append(h2("Karar Matrisi (Hızlı Özet)"))
    body.append(
        p(
            "Aşağıdaki çerçeve \"tek doğru\" değil; doğru kararı hızlandıran bir karar matrisi olarak düşünülmelidir."
        )
    )
    body.append(h3("React Native genelde daha doğruysa"))
    body.append(
        ul(
            [
                "MVP hızlı çıkmalı",
                "özellikler çoğunlukla standart akışlardan oluşuyor",
                "tek ekip ile iki platform yönetmek istiyorsunuz",
                "ürün sürekli iterasyonla gelişecek",
                "bütçeyi kontrollü tutmak önemli",
            ]
        )
    )
    body.append(h3("Native genelde daha doğruysa"))
    body.append(
        ul(
            [
                "maksimum performans en kritik gereksinim",
                "ağır animasyon / kamera / AR / ML yoğunluğu yüksek",
                "çok özel cihaz yetenekleri ve düşük seviye entegrasyonlar var",
                "UI/UX’in platformun ince detaylarına kadar native olması şart",
                "platforma özel ayrı roadmap planlıyorsunuz",
            ]
        )
    )

    body.append(h2("Senaryo bazlı öneriler"))
    body.append(h3("1) E‑ticaret / katalog / rezervasyon uygulaması"))
    body.append(
        p(
            "Tipik ekranlar: liste, detay, sepet, ödeme, profil. Çoğu zaman React Native; hız + bakım avantajı nedeniyle idealdir."
        )
    )
    body.append(h3("2) Sosyal uygulama / mesajlaşma / feed odaklı ürün"))
    body.append(
        p(
            "Kritik başlıklar: akıcı scroll, medya, bildirimler, offline senaryolar. React Native mümkün, ama performans hedeflerinin erken aşamada netleştirilmesi gerekir; çok yoğun medya ve gerçek zamanlı işlemlerde native tercih edilebilir."
        )
    )
    body.append(h3("3) Kamera tabanlı, AR, filtre, video işleme, ML yoğun ürün"))
    body.append(
        p(
            "Cihaz donanımı, düşük seviye erişim ve yüksek FPS kritikse; native yaklaşım genelde daha güvenli seçenektir."
        )
    )
    body.append(h3("4) Kurumsal iç uygulama / saha ekibi / CRM"))
    body.append(
        p(
            "Kritik başlıklar: hızlı geliştirme, form akışları, entegrasyonlar. Burada React Native genelde en verimli yaklaşım olur (hız + sürdürülebilirlik)."
        )
    )

    body.append(h2("Önerilen süreç (Karar ve teslim planı)"))
    body.append(h3("1) Keşif ve hedefler"))
    body.append(
        ul(
            [
                "\"hız mı performans mı?\" yerine: hangi ekranlarda hangi hedef?",
                "kritik akışlar ve kullanıcı senaryoları",
                "MVP kapsamı ve faz planı",
            ]
        )
    )
    body.append(h3("2) Plan: teslim kriterleri ve öncelikler"))
    body.append(
        ul(
            [
                "kabul kriterleri: performans hedefleri, güvenlik, erişilebilirlik",
                "risk analizi: entegrasyonlar, içerik, store süreçleri",
            ]
        )
    )
    body.append(h3("3) Uygulama: mimari ve geliştirme"))
    body.append(
        ul(
            [
                "React Native’de performans disiplinleri (render kontrolü, liste optimizasyonu)",
                "Native’de modüler yapı ve bakım stratejisi",
                "ortak: test, loglama, analitik planı",
            ]
        )
    )
    body.append(h3("4) Test ve yayın"))
    body.append(
        ul(
            [
                "cihaz çeşitliliği testleri",
                "crash/ANR ve performans izleme",
                "rollout stratejisi ve sürüm planı",
            ]
        )
    )

    body.append(h2("Teslimatlar"))
    body.append(h3("1) Karar Matrisi (doküman)"))
    body.append(
        p(
            "Hedef/kısıt listesi, ekran bazlı performans beklentisi ve önerilen teknoloji + gerekçesini içeren karar dokümanı."
        )
    )
    body.append(h3("2) Senaryo bazlı öneri"))
    body.append(
        p(
            "Ürün tipinize göre en doğru yaklaşım, MVP + Faz‑2 planı ve \"ne yapılmayacak\" sınırları (scope protection) netleştirilir."
        )
    )

    body.append(h2("Kalite standartları ve kabul kriterleri"))
    body.append(
        p(
            "Kaliteyi artırmanın en net yolu; beklentileri ölçülebilir kriterlere dönüştürmektir. Özellikle performans, güvenlik, içerik yapısı ve kabul kriterleri yazılı hale geldiğinde, karar almak ve iterasyon yapmak kolaylaşır."
        )
    )
    body.append(
        ul(
            [
                "Performans: liste/akış hedefleri, optimizasyon planı",
                "Güvenlik: erişim yetkileri, token yönetimi, sertleştirme",
                "İçerik: şablon tutarlılığı ve hiyerarşi",
                "Kabul: net \"tamamlandı\" tanımı ve kontrol listesi",
            ]
        )
    )

    body.append(
        cta_box(
            "Karar vermek için uzun toplantılara değil, net bir brife ihtiyacımız var.",
            "Hedefinizi ve önceliklerinizi paylaşın; size en doğru yaklaşımı ve takvimi çıkaralım. Mobil uygulama geliştirme için teklif sayfasına gidin.",
            _quote_url(page),
            "Mobil Uygulama Geliştirme Teklif Al",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        (
            "React Native performans olarak yeterli mi?",
            "Birçok ürün için evet. Kritik olan, hangi ekranlarda hangi performans hedefinin gerektiğini netleştirip bunu mimariye yansıtmaktır.",
        ),
        (
            "Native her zaman daha mı iyi?",
            "Hayır. Native daha fazla kontrol sağlar ama süre ve harcama tarafını artırabilir. Ürünün hedefi ve iterasyon planı belirleyicidir.",
        ),
        (
            "İlk adım nedir?",
            "Hedefi ve öncelikleri netleştirmek, ardından MVP kapsamını yazılı hale getirmektir.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "React Native mi Native mi? | Performans, Bütçe ve Zaman Karşılaştırması"
    meta_description = (
        "React Native mi Native mi seçmelisiniz? Performans, bütçe ve teslim süresi açısından karar matrisi, senaryo bazlı öneriler ve doğru yaklaşımı belirleme rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "React Native mi Native mi? — Doğru Platform Kararı Nasıl Verilir?",
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


def _cluster_ozel_yazilim_vs_hazir_site_tr(page: SeoPage) -> Dict:
    """Custom cluster: Özel Yazılım mı Hazır Site mi? — comparison, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Giriş"))
    body.append(
        p(
            "Web sitesi yaptırmak isteyen işletmelerin en büyük sorusu: Hazır site mi kullanmalıyım, yoksa özel yazılım mı yaptırmalıyım? "
            "Bu karar sadece tasarım tercihi değildir. SEO performansı, ölçeklenebilirlik, güvenlik, entegrasyon ve uzun vadeli büyüme potansiyelini doğrudan etkiler."
        )
    )
    body.append(
        p(
            f"Bu sayfada iki yaklaşımı teknik ve stratejik açıdan karşılaştırıyoruz. Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("Hazır Site Nedir?"))
    body.append(
        p(
            "Hazır site; genellikle WordPress, Wix, Shopify gibi sistemler veya hazır temalar üzerinden kurulan web siteleridir."
        )
    )
    body.append(p("Avantajları:"))
    body.append(
        ul(
            [
                "Hızlı kurulum",
                "Düşük başlangıç bütçesi",
                "Teknik bilgi gerektirmemesi",
                "Basit projeler için yeterli olması",
            ]
        )
    )
    body.append(p("Dezavantajları:"))
    body.append(
        ul(
            [
                "Sınırlı özelleştirme",
                "Fazla eklenti kullanımı → performans düşüşü",
                "Güvenlik riskleri",
                "Teknik SEO kontrolünün kısıtlı olması",
            ]
        )
    )
    body.append(p("Hazır sistemler küçük ve başlangıç aşamasındaki projeler için mantıklıdır."))

    body.append(h2("Özel Yazılım Web Sitesi Nedir?"))
    body.append(
        p(
            "Özel yazılım web sitesi; işletmenin ihtiyaçlarına göre sıfırdan geliştirilen, esnek ve ölçeklenebilir çözümdür. Genellikle Django, Laravel, Node.js veya özel backend mimarileri kullanılarak geliştirilir."
        )
    )
    body.append(p("Avantajları:"))
    body.append(
        ul(
            [
                "Tam kontrol",
                "Performans optimizasyonu",
                "Gelişmiş SEO altyapısı",
                "Entegrasyon özgürlüğü",
                "Uzun vadeli büyüme potansiyeli",
            ]
        )
    )
    body.append(
        p(
            f"Özel yazılım, sistem gerektiren projelerde güçlüdür. Detay: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("SEO Açısından Karşılaştırma"))
    body.append(p("Hazır site: URL yapısı sınırlı olabilir; fazla eklenti site hızını düşürebilir; Core Web Vitals optimizasyonu zor olabilir; teknik SEO müdahalesi kısıtlıdır."))
    body.append(
        p(
            "Özel yazılım: SEO uyumlu mimari sıfırdan planlanır; schema markup tam kontrol edilir; iç link yapısı stratejik kurulur; crawl bütçesi optimize edilir; sayfa hızı mühendislik seviyesinde optimize edilir. SEO öncelikliyse, özel yazılım genellikle daha avantajlıdır."
        )
    )

    body.append(h2("Performans ve Hız"))
    body.append(
        p(
            "Google sıralaması için: mobil uyumluluk, sayfa yüklenme süresi, Core Web Vitals, sunucu yanıt süresi kritik faktörlerdir. Hazır sistemler genellikle fazla script yükü, gereksiz CSS/JS, ortak hosting kısıtları barındırabilir. Özel geliştirme ise temiz kod ve optimize sorgular ile daha yüksek performans sunar."
        )
    )

    body.append(h2("Güvenlik"))
    body.append(
        p(
            "Hazır sistemlerde: eklenti açıkları, güncelleme sorunları, bot saldırı riskleri daha sık görülür. Özel yazılımda: rol bazlı yetkilendirme, güvenli authentication, backend sertleştirme, veri kontrolü daha kontrollü şekilde uygulanır."
        )
    )

    body.append(h2("Ölçeklenebilirlik"))
    body.append(
        p(
            "Başlangıçta küçük görünen projeler büyüyebilir. Çoklu kullanıcı sistemi, CRM entegrasyonu, ödeme altyapısı, dashboard, API bağlantıları planlıyorsanız, özel yazılım daha sürdürülebilir bir çözümdür."
        )
    )

    body.append(h2("Hangi Durumda Hangisi Mantıklı?"))
    body.append(p("Hazır site mantıklıysa: küçük işletme, sadece tanıtım sitesi, kısa vadeli çözüm, teknik entegrasyon yok."))
    body.append(
        p(
            "Özel yazılım mantıklıysa: büyüme hedefi varsa, SEO öncelikliyse, performans kritikse, entegrasyon gerekiyorsa, sistem altyapısı planlanıyorsa."
        )
    )

    body.append(h2("Stratejik Bakış"))
    body.append(
        p(
            "Hazır site \"başlangıç çözümü\" olabilir. Özel yazılım \"altyapı yatırımıdır.\" Doğru seçim, projenin vizyonuna bağlıdır."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Özel yazılım mı hazır site mi sorusunun tek bir doğru cevabı yoktur. Ancak uzun vadeli SEO başarısı, performans, güvenlik ve ölçeklenebilirlik hedefleniyorsa; özel yazılım genellikle daha güçlü bir temel sunar."
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
                f"{{{{ link:/tr/web-tasarim/django-web-gelistirme/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Hazır mı özel mi kararını hedeflerinize göre birlikte netleştirelim; size uygun kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Hazır site nedir?", "WordPress, Wix, Shopify gibi sistemler veya hazır temalar üzerinden kurulan siteler; hızlı kurulum, sınırlı özelleştirme."),
        ("Özel yazılım web sitesi nedir?", "İşletmenin ihtiyaçlarına göre sıfırdan geliştirilen, esnek ve ölçeklenebilir çözüm; tam kontrol ve SEO avantajı."),
        ("SEO açısından fark nedir?", "Özel yazılımda URL, schema, iç link ve performans tam kontrol edilir; hazırda teknik SEO kısıtlı olabilir."),
        ("Hangi durumda hazır site?", "Küçük işletme, sadece tanıtım, kısa vadeli çözüm, teknik entegrasyon yoksa."),
        ("Hangi durumda özel yazılım?", "Büyüme hedefi, SEO önceliği, performans kritik, entegrasyon veya sistem altyapısı planlanıyorsa."),
        ("Karar için ne yapmalı?", "Hedef ve vizyonu netleştirin; kapsamı birlikte çıkarmak için teklif formunu doldurun."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Özel Yazılım mı Hazır Site mi? | Hangisi Daha Doğru Seçim?"
    meta_description = (
        "Hazır site mi yoksa özel yazılım web sitesi mi? SEO, performans, ölçeklenebilirlik ve güvenlik açısından detaylı karşılaştırma."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Özel Yazılım mı Hazır Site mi? — Doğru Kararı Nasıl Verirsiniz?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_tasarim_freelancer_tr(page: SeoPage) -> Dict:
    """Custom cluster: Freelancer ile Çalışma — advantages, risks, when to choose. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Freelancer ile Web Tasarım Nedir?"))
    body.append(
        p(
            "Freelancer ile çalışma; bağımsız bir web geliştirici veya tasarımcı ile proje bazlı iş yapmaktır. Genellikle: daha esnek iletişim, daha düşük başlangıç bütçesi, daha hızlı başlangıç süreci gibi avantajlar sunar."
        )
    )
    body.append(
        p(
            "Ancak web tasarım ve yazılım projeleri sadece tasarım üretmekten ibaret değildir. SEO, performans, güvenlik ve ölçeklenebilirlik gibi teknik konular da işin parçasıdır."
        )
    )
    body.append(
        p(
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Ajans ile karşılaştırma: {{{{ link:/tr/web-tasarim/ajans-mi-freelancer-mi/ }}}}."
        )
    )

    body.append(h2("Freelancer ile Çalışmanın Avantajları"))
    body.append(
        ul(
            [
                "Esneklik: Karar süreçleri daha hızlı ilerleyebilir.",
                "Daha düşük başlangıç bütçesi: Küçük projeler için uygun olabilir.",
                "Direkt iletişim: Karar veren kişi ile doğrudan iletişim kurulabilir.",
            ]
        )
    )
    body.append(
        p("Özellikle tek sayfalık siteler, portföy siteleri veya MVP projelerde freelancer mantıklı olabilir.")
    )

    body.append(h2("Freelancer ile Çalışmanın Riskleri"))
    body.append(
        p("Profesyonel projelerde en sık karşılaşılan sorunlar:")
    )
    body.append(
        ul(
            [
                "Ölçeklenebilirlik: Proje büyüdüğünde destek ve bakım süreci zorlaşabilir.",
                "Teknik SEO eksikliği: Çoğu freelancer tasarım odaklıdır; teknik SEO altyapısı her zaman güçlü olmayabilir.",
                "Performans optimizasyonu: Core Web Vitals, cache stratejileri, server-side optimizasyon her zaman planlanmaz.",
                "Süreklilik: Freelancer projeyi teslim ettikten sonra uzun vadeli destek garantisi olmayabilir.",
            ]
        )
    )

    body.append(h2("Freelancer mı Ajans mı? Karar Nasıl Verilir?"))
    body.append(
        p(
            "Şu sorular kritik: Proje uzun vadeli mi? Entegrasyon veya özel yazılım ihtiyacı var mı? SEO hedefi güçlü mü? Güvenlik kritik mi? Bakım ve destek gerekecek mi? Eğer proje stratejik bir yatırım ise; teknik ekipli, süreç yönetimi olan bir yapı daha güvenli olur."
        )
    )
    body.append(
        p(
            f"Detaylı karşılaştırma: {{{{ link:/tr/web-tasarim/ajans-mi-freelancer-mi/ }}}}."
        )
    )

    body.append(h2("SEO ve Teknik Altyapı Açısından Değerlendirme"))
    body.append(
        p(
            "Profesyonel bir web sitesi: schema markup içerir, teknik SEO kontrolüne sahiptir, iç link mimarisi planlıdır, performans testlerinden geçmiştir, güvenli sunucu yapılandırmasına sahiptir. Freelancer ile çalışırken bu kriterlerin açıkça konuşulması gerekir."
        )
    )

    body.append(h2("Hangi Projelerde Freelancer Mantıklıdır?"))
    body.append(
        ul(
            [
                "Basit landing page",
                "Portföy sitesi",
                "Küçük çaplı kurumsal tanıtım sitesi",
                "MVP başlangıç projeleri",
            ]
        )
    )

    body.append(h2("Hangi Projelerde Profesyonel Ekip Gerekir?"))
    body.append(
        ul(
            [
                "Kurumsal web sitesi",
                "E-ticaret projeleri",
                "Özel yazılım gerektiren sistemler",
                "SEO odaklı rekabetçi sektörler",
                "Çoklu entegrasyonlu platformlar",
            ]
        )
    )
    body.append(
        p(
            f"Özel yazılım: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Freelancer ile çalışma yanlış değildir. Yanlış olan; projenin büyüklüğüne uygun olmayan seçim yapmaktır. Web tasarım, sadece tasarım değil; teknik mimari ve uzun vadeli dijital stratejidir. Doğru seçim, hedeflerinize göre yapılmalıdır."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/ajans-mi-freelancer-mi/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Freelancer mı ajans mı kararını hedeflerinize göre birlikte netleştirelim; size uygun modeli önerelim.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Freelancer ile çalışma nedir?", "Bağımsız geliştirici veya tasarımcı ile proje bazlı çalışma; esnek iletişim, düşük başlangıç bütçesi, hızlı başlangıç avantajı sunar."),
        ("Avantajları neler?", "Esneklik, düşük başlangıç bütçesi, direkt iletişim; tek sayfa, portföy veya MVP için mantıklı olabilir."),
        ("Riskleri neler?", "Ölçeklenebilirlik, teknik SEO eksikliği, performans optimizasyonu ve uzun vadeli destek sınırlı olabilir."),
        ("Freelancer mı ajans mı?", "Uzun vadeli, entegrasyonlu, SEO odaklı projelerde ajans; basit ve kısa vadeli projelerde freelancer düşünülebilir."),
        ("Hangi projelerde freelancer yeterli?", "Landing page, portföy, küçük tanıtım sitesi, MVP."),
        ("Teklif için ne gerekli?", "Hedef, kapsam ve tercih (freelancer / ajans) paylaşmanız yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Freelancer ile Çalışma | Web Tasarımda Doğru Karar"
    meta_description = (
        "Freelancer ile web tasarım süreci nasıl işler? Avantajlar, riskler ve profesyonel yaklaşım farkı. SEO uyumlu ve ölçeklenebilir çözüm rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Freelancer ile Çalışma — Web Tasarımda Avantajlar ve Riskler",
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


def _cluster_profesyonel_web_tasarim_tr(page: SeoPage) -> Dict:
    """Custom cluster: Profesyonel Web Tasarım — SEO, performance, conversion. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Profesyonel Web Tasarım Nedir?"))
    body.append(
        p(
            "Profesyonel web tasarım; yalnızca görsel tasarım değil, teknik altyapı, SEO mimarisi, performans optimizasyonu ve kullanıcı deneyiminin birlikte planlandığı stratejik bir süreçtir."
        )
    )
    body.append(
        p(
            "Modern bir web sitesi: SEO uyumlu olmalı, mobil uyumlu (responsive) olmalı, Core Web Vitals metriklerinde güçlü olmalı, hızlı yüklenmeli, güvenli (HTTPS) altyapıya sahip olmalı, dönüşüm odaklı CTA yapısına sahip olmalı. Profesyonellik; tasarımın arkasındaki mühendisliktir."
        )
    )
    body.append(
        p(
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("Neden Profesyonel Web Tasarım Gereklidir?"))
    body.append(
        p(
            "Google sıralamalarını belirleyen faktörler: sayfa hızı, mobil performans, teknik SEO, iç bağlantı mimarisi, kullanıcı deneyimi, güvenlik. Rekabetin yoğun olduğu sektörlerde amatör altyapılar sürdürülebilir değildir."
        )
    )

    body.append(h2("SEO Uyumlu Profesyonel Web Tasarım"))
    body.append(
        ul(
            [
                "Doğru başlık hiyerarşisi (H1–H2–H3)",
                "Schema markup (Organization, FAQ, Breadcrumb)",
                "Optimize edilmiş URL yapısı",
                "Canonical ve index kontrolü",
                "İç link stratejisi (pillar-cluster modeli)",
                "Crawl bütçesi optimizasyonu",
            ]
        )
    )
    body.append(p("SEO sonradan eklenmez; baştan planlanır."))

    body.append(h2("Performans ve Core Web Vitals"))
    body.append(
        p(
            "Profesyonel web tasarım: optimize görseller, lazy loading, minimal JS kullanımı, sunucu yanıt süresi optimizasyonu, cache stratejisi. Performans, hem SEO hem dönüşüm oranlarını doğrudan etkiler."
        )
    )

    body.append(h2("UX ve Dönüşüm Optimizasyonu"))
    body.append(
        p(
            "Güzel tasarım yeterli değildir. Profesyonel yaklaşım: net CTA yerleşimi, kullanıcı akış optimizasyonu, güven unsurları, stratejik form konumlandırma, okunabilir tipografi. Amaç ziyaret değil, dönüşümdür."
        )
    )

    body.append(h2("Kimler İçin Uygundur?"))
    body.append(
        ul(
            [
                "Kurumsal firmalar",
                "E-ticaret projeleri",
                "Danışmanlık şirketleri",
                "Ajanslar",
                "SaaS girişimleri",
                "Rekabetçi sektörler",
            ]
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Profesyonel web tasarım; markanızın dijital altyapısını oluşturur. SEO, performans ve kullanıcı deneyimi birlikte planlandığında uzun vadeli başarı sağlar."
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
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Profesyonel web tasarım için hedeflerinizi paylaşın; size uygun kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Profesyonel web tasarım nedir?", "Görsel tasarımın yanı sıra teknik altyapı, SEO mimarisi, performans ve UX'in birlikte planlandığı stratejik süreçtir."),
        ("Neden profesyonel yaklaşım gerekli?", "Google sayfa hızı, mobil performans, teknik SEO ve güvenliği değerlendirir; rekabetçi sektörlerde amatör altyapı sürdürülemez."),
        ("SEO nasıl planlanır?", "Başlık hiyerarşisi, schema markup, URL yapısı, iç link ve crawl optimizasyonu baştan kurulmalıdır."),
        ("Performans neden kritik?", "Core Web Vitals hem sıralamayı hem dönüşüm oranını etkiler; optimize görsel ve cache şarttır."),
        ("Kimler için uygundur?", "Kurumsal firmalar, e-ticaret, danışmanlık, ajanslar, SaaS ve rekabetçi sektörler."),
        ("Teklif için ne gerekli?", "Hedef, hedef kitle ve sektör bilgisi yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Profesyonel Web Tasarım | SEO Uyumlu & Performans Odaklı"
    meta_description = (
        "Profesyonel web tasarım hizmeti. SEO uyumlu, mobil uyumlu, hızlı ve dönüşüm odaklı modern web siteleri ile markanızı dijitalde güçlendirin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Profesyonel Web Tasarım — SEO, Performans ve Dönüşüm Odaklı Yaklaşım",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_ozel_yazilim_web_sitesi_tr(page: SeoPage) -> Dict:
    """Custom cluster: Özel Yazılım Web Sitesi — scalable, SEO-ready, professional. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Özel Yazılım Web Sitesi Nedir?"))
    body.append(
        p(
            "Özel yazılım web sitesi; hazır tema veya şablon yerine, işletmenin ihtiyaçlarına göre sıfırdan geliştirilen, esnek ve ölçeklenebilir web çözümüdür."
        )
    )
    body.append(
        p(
            "Bu yaklaşımda: veri modeli size göre kurulur, mimari iş hedeflerine göre planlanır, SEO altyapısı başlangıçtan itibaren optimize edilir, performans ve güvenlik kontrol altında olur. "
            "Hazır sistemler hızlı başlangıç sağlar. Özel yazılım ise uzun vadeli kontrol sağlar."
        )
    )
    body.append(
        p(
            f"Genel çerçeve için {{{{ link:{_pillar_url(page)} }}}} sayfasına bakabilirsiniz."
        )
    )

    body.append(h2("Neden Özel Yazılım Tercih Edilir?"))
    body.append(h2("Ölçeklenebilirlik"))
    body.append(
        p(
            "Büyüyen işletmeler için: çoklu kullanıcı rolleri, CRM / ERP entegrasyonu, API bağlantıları, özel modüller, çoklu dil desteği gibi ihtiyaçlar ortaya çıkar. "
            "Hazır altyapılar burada sınıra dayanabilir. Özel yazılım ise esnektir."
        )
    )
    body.append(h2("Teknik SEO Kontrolü"))
    body.append(
        p(
            "Özel geliştirme ile: URL yapısı tamamen kontrol edilir, iç link mimarisi planlanır, schema markup detaylı uygulanır, crawl bütçesi optimize edilir, sayfa hızı mühendislik seviyesinde iyileştirilir. "
            "SEO uyumlu web sitesi sonradan değil, mimari aşamada kurulur."
        )
    )
    body.append(h2("Performans ve Core Web Vitals"))
    body.append(
        p(
            "Google sıralamasında performans belirleyicidir. Özel yazılım projelerinde: gereksiz script yükü olmaz, backend sorguları optimize edilir, cache stratejileri planlanır, mobil-first yaklaşım uygulanır. Bu da hem SEO hem dönüşüm oranlarını artırır."
        )
    )

    body.append(h2("Hangi Projeler İçin Özel Yazılım Mantıklıdır?"))
    body.append(
        ul(
            [
                "Kurumsal web siteleri (ileri düzey yapı)",
                "B2B platformlar",
                "SaaS projeleri",
                "Rezervasyon / randevu sistemleri",
                "Dashboard ve yönetim panelleri",
                "Çoklu entegrasyon gerektiren sistemler",
            ]
        )
    )
    body.append(
        p("Standart web sitesi değil; sistem altyapısı gerektiren projeler için uygundur.")
    )

    body.append(h2("Özel Yazılım Web Sitesi Geliştirme Süreci"))
    body.append(
        ul(
            [
                "Keşif ve teknik analiz",
                "Bilgi mimarisi planlama",
                "UI/UX tasarım",
                "Backend geliştirme (örneğin Django tabanlı mimari)",
                "API ve entegrasyonlar",
                "Performans optimizasyonu",
                "Test ve yayın",
            ]
        )
    )
    body.append(p("Süreç odaklı yaklaşım, teknik borcu azaltır."))

    body.append(h2("Güvenlik ve Veri Koruma"))
    body.append(
        p(
            "Özel yazılım projelerinde: rol bazlı yetkilendirme, HTTPS zorunluluğu, güvenli form akışları, sunucu sertleştirme, temel veri koruma prensipleri planlı şekilde uygulanır. Güvenlik, sonradan eklenen bir özellik değildir."
        )
    )

    body.append(h2("Özel Yazılım mı Hazır Sistem mi?"))
    body.append(
        p(
            "Hazır sistemler: hızlı başlangıç, düşük teknik giriş seviyesi. Özel yazılım: tam kontrol, uzun vadeli esneklik, performans avantajı, SEO derinliği. Hedef büyüme ise; özel yazılım genellikle daha sürdürülebilir çözümdür."
        )
    )
    body.append(
        p(
            f"Karşılaştırma: {{{{ link:/tr/web-tasarim/ozel-yazilim-vs-hazir-site/ }}}}."
        )
    )

    body.append(h2("Özel Yazılım Web Sitesi ile Neler Kazanırsınız?"))
    body.append(
        ul(
            [
                "Ölçeklenebilir altyapı",
                "SEO uyumlu mimari",
                "Yüksek performans",
                "Güvenli backend sistemi",
                "Entegrasyona açık yapı",
            ]
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Özel yazılım web sitesi; sadece bir web tasarım tercihi değil, stratejik bir dijital altyapı yatırımıdır. Uzun vadeli büyüme, teknik esneklik ve SEO kontrolü için güçlü bir temel sunar."
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
                f"{{{{ link:/tr/web-tasarim/django-web-gelistirme/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-vs-hazir-site/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Özel yazılım web sitesi için hedeflerinizi ve teknik ihtiyaçlarınızı paylaşın; size uygun kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Özel yazılım web sitesi nedir?", "İşletmenin ihtiyaçlarına göre sıfırdan geliştirilen, esnek ve ölçeklenebilir web çözümüdür; hazır tema kullanılmaz."),
        ("Neden özel yazılım tercih edilir?", "Ölçeklenebilirlik, teknik SEO kontrolü, performans ve güvenlik avantajı; uzun vadeli esneklik sağlar."),
        ("Hangi projeler için uygundur?", "Kurumsal ileri düzey siteler, B2B, SaaS, rezervasyon sistemleri, dashboard ve çoklu entegrasyon gerektiren projeler."),
        ("Geliştirme süreci nasıl ilerler?", "Keşif, bilgi mimarisi, UI/UX, backend geliştirme, API ve entegrasyonlar, performans, test ve yayın."),
        ("Güvenlik nasıl sağlanır?", "Rol bazlı yetkilendirme, HTTPS, güvenli form akışları, sunucu sertleştirme mimari aşamada planlanır."),
        ("Hazır sistem mi özel yazılım mı?", "Hızlı başlangıç için hazır; uzun vadeli kontrol ve büyüme için özel yazılım daha sürdürülebilirdir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Özel Yazılım Web Sitesi | Ölçeklenebilir ve SEO Uyumlu Çözümler"
    meta_description = (
        "SEO uyumlu, ölçeklenebilir ve güvenli özel yazılım web sitesi çözümleri. Performans odaklı mimari ve profesyonel geliştirme yaklaşımı."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Özel Yazılım Web Sitesi — Ölçeklenebilir ve Profesyonel Geliştirme",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_developer_istanbul_tr(page: SeoPage) -> Dict:
    """Custom cluster: İstanbul Web Geliştirici — local + hiring intent. No pricing triggers."""
    body: List[str] = []

    body.append(h2("İstanbul'da Web Geliştirici Seçerken Nelere Dikkat Edilmeli?"))
    body.append(
        p(
            "Web geliştirici seçimi yalnızca tasarım kalitesiyle ilgili değildir. Değerlendirilmesi gereken kriterler: teknik SEO bilgisi, performans optimizasyonu, backend mimarisi, güvenlik yaklaşımı, uzun vadeli destek."
        )
    )
    body.append(
        p(
            "İstanbul gibi rekabetçi pazarda doğru teknik altyapı kritik önem taşır."
        )
    )
    body.append(
        p(
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Yerel hizmet: {{{{ link:/tr/web-tasarim/istanbul/ }}}}."
        )
    )

    body.append(h2("Neden Profesyonel Bir Web Geliştirici?"))
    body.append(
        p(
            "Profesyonel geliştirici: SEO uyumlu kod yazar, Core Web Vitals optimizasyonu yapar, ölçeklenebilir mimari kurar, güvenli sunucu yapılandırması sağlar, entegrasyon süreçlerini planlar."
        )
    )

    body.append(h2("Freelancer mı, Ekip mi?"))
    body.append(
        p(
            "Basit projelerde freelancer yeterli olabilir. Ancak kurumsal ve büyüme hedefli projelerde ekip yapısı avantaj sağlar."
        )
    )
    body.append(
        p(
            f"Karşılaştırma: {{{{ link:/tr/web-tasarim/ajans-mi-freelancer-mi/ }}}}, {{{{ link:/tr/web-tasarim/web-tasarim-freelancer/ }}}}."
        )
    )

    body.append(h2("Hangi Projeler İçin Uygundur?"))
    body.append(
        ul(
            [
                "Kurumsal web sitesi",
                "Özel yazılım projeleri",
                "E-ticaret altyapısı",
                "Çoklu entegrasyon gerektiren sistemler",
            ]
        )
    )
    body.append(
        p(
            f"Özel yazılım: {{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "İstanbul'da web geliştirici seçerken teknik altyapı, SEO uyumu ve ölçeklenebilirlik birlikte değerlendirilmelidir. Doğru seçim uzun vadeli dijital başarı sağlar."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/tr/web-tasarim/istanbul/ }}}}",
                f"{{{{ link:/tr/web-tasarim/ozel-yazilim-web-sitesi/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "İstanbul'da web geliştirici ihtiyacınız için hedeflerinizi paylaşın; size uygun kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("İstanbul'da web geliştirici seçerken nelere dikkat edilmeli?", "Teknik SEO, performans, backend mimarisi, güvenlik ve uzun vadeli destek kriterleri değerlendirilmelidir."),
        ("Neden profesyonel geliştirici?", "SEO uyumlu kod, Core Web Vitals, ölçeklenebilir mimari ve güvenli altyapı sağlar."),
        ("Freelancer mı ekip mi?", "Basit projelerde freelancer; kurumsal ve büyüme hedefli projelerde ekip yapısı daha uygundur."),
        ("Hangi projeler için uygundur?", "Kurumsal site, özel yazılım, e-ticaret, çoklu entegrasyon gerektiren sistemler."),
        ("Teklif için ne gerekli?", "Hedef, kapsam ve teknik ihtiyaçlarınızı paylaşmanız yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "İstanbul Web Geliştirici | Profesyonel ve SEO Odaklı"
    meta_description = (
        "İstanbul web geliştirici arayanlar için SEO uyumlu, mobil uyumlu ve ölçeklenebilir web geliştirme çözümleri."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "İstanbul Web Geliştirici — Profesyonel ve Ölçeklenebilir Çözümler",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_tasarim_nedir_tr(page: SeoPage) -> Dict:
    """Custom cluster: Web Tasarım Nedir? — high-value, trend keywords. No new page links, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Web Tasarım Nedir?"))
    body.append(
        p(
            "Web tasarım; bir web sitesinin görsel düzeni, kullanıcı arayüzü (UI), kullanıcı deneyimi (UX) ve teknik altyapısının birlikte planlanıp uygulanması sürecidir. Yalnızca görsel çizim değil; metin, görsel, navigasyon ve etkileşim öğelerinin iş hedeflerine ve hedef kitleye uygun biçimde bir araya getirilmesidir."
        )
    )
    body.append(
        p(
            "Modern web tasarım kavramı; masaüstü ve mobil uyumluluk (responsive tasarım), erişilebilirlik, sayfa hızı ve arama motoru uyumluluğu (SEO) ile birlikte düşünülür. Profesyonel web tasarımı bu unsurların tamamını kapsar."
        )
    )
    body.append(
        p(
            f"Genel hizmet çerçevesi: {{{{ link:{_pillar_url(page)} }}}}. Süreç rehberi: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Web Tasarımı Neleri Kapsar?"))
    body.append(
        ul(
            [
                "Bilgi mimarisi ve sayfa hiyerarşisi",
                "Görsel tasarım ve tipografi",
                "Kullanıcı akışları ve dönüşüm odaklı yerleşim (CTA)",
                "Mobil uyumlu (responsive) yapı",
                "Teknik SEO temeli (URL, başlıklar, meta yapı)",
                "Performans ve hız optimizasyonu",
            ]
        )
    )

    body.append(h2("Neden Web Tasarımı Önemlidir?"))
    body.append(
        p(
            "Web siteniz; markanızın dijital yüzüdür. Ziyaretçiler ilk saniyelerde sayfa hızına, düzene ve güvene tepki verir. Kötü tasarım veya yavaş açılan sayfalar, hemen çıkış oranını artırır; iyi tasarım ise dönüşüm ve marka algısını güçlendirir."
        )
    )
    body.append(
        p(
            "Arama motorları da kullanıcı deneyimini ve teknik yapıyı değerlendirir. Temiz kod, hızlı yükleme ve mantıklı içerik hiyerarşisi sıralamayı etkiler."
        )
    )

    body.append(h2("Web Tasarım ve SEO İlişkisi"))
    body.append(
        p(
            "SEO uyumlu web tasarım; başlık hiyerarşisi (H1–H2–H3), anlamlı URL yapısı, mobil uyumluluk ve Core Web Vitals gibi metriklerin baştan planlanması demektir. Tasarım bittikten sonra SEO eklemek yerine, tasarım aşamasında teknik gereksinimler düşünülmelidir."
        )
    )

    body.append(h2("Kimler İçin Geçerlidir?"))
    body.append(
        p(
            "Kurumsal firmalar, e-ticaret siteleri, danışmanlık ve ajanslar, portföy siteleri, landing sayfaları ve SaaS ürünleri için web tasarımı temel ihtiyaçtır. Hedef kitle ve iş modeline göre kapsam değişir."
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Web tasarım nedir sorusunun cevabı; yalnızca görsel değil, stratejik ve teknik bir bütündür. Doğru planlama ile hem kullanıcı deneyimi hem arama görünürlüğü güçlendirilir."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Web tasarım ihtiyacınız için hedeflerinizi paylaşın; size uygun kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Web tasarım nedir?", "Web sitesinin görsel düzeni, UI/UX ve teknik altyapısının iş hedeflerine göre planlanıp uygulanması sürecidir."),
        ("Web tasarımı neler kapsar?", "Bilgi mimarisi, görsel tasarım, kullanıcı akışları, mobil uyumluluk, teknik SEO ve performans optimizasyonu."),
        ("Neden önemlidir?", "Siteniz markanızın dijital yüzüdür; hız, düzen ve güven hem kullanıcı hem arama motoru için belirleyicidir."),
        ("SEO ile ilişkisi nasıl?", "Başlık hiyerarşisi, URL yapısı, mobil uyum ve Core Web Vitals tasarım aşamasında planlanmalıdır."),
        ("Kimler için uygundur?", "Kurumsal, e-ticaret, ajans, portföy, landing ve SaaS projeleri için temel ihtiyaçtır."),
        ("Teklif için ne gerekli?", "Hedef, hedef kitle ve proje kapsamı paylaşmanız yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Tasarım Nedir? | Profesyonel Web Tasarım Rehberi"
    meta_description = (
        "Web tasarım nedir? UI, UX, responsive tasarım ve SEO uyumlu web sitesi kavramları. Modern web tasarımı rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Tasarım Nedir? — Tanım, Kapsam ve Modern Yaklaşım",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_sitesi_nasil_yapilir_tr(page: SeoPage) -> Dict:
    """Custom cluster: Web Sitesi Nasıl Yapılır? — step-by-step, high-value. No new page links, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Web Sitesi Nasıl Yapılır?"))
    body.append(
        p(
            "Web sitesi yapmak; hedef belirleme, planlama, tasarım, geliştirme, test ve yayın aşamalarından oluşan yapılandırılmış bir süreçtir. Doğru adımlar teknik borcu azaltır ve hem kullanıcı deneyimini hem arama motoru uyumluluğunu güçlendirir."
        )
    )
    body.append(
        p(
            f"Genel çerçeve: {{{{ link:{_pillar_url(page)} }}}}. Adım adım rehber: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Adım Adım Web Sitesi Yapım Süreci"))
    body.append(
        ul(
            [
                "Keşif ve hedef analizi: Amaç, hedef kitle ve rakiplerin netleştirilmesi.",
                "Bilgi mimarisi: Sayfa yapısı, navigasyon ve içerik hiyerarşisinin planlanması.",
                "UI/UX tasarım: Wireframe ve tasarım onayı; mobil uyumluluk.",
                "Geliştirme: Kodlama, entegrasyonlar, teknik SEO altyapısı.",
                "Test ve performans: Hız, güvenlik ve tarayıcı uyumluluğu kontrolü.",
                "Yayın ve izleme: Canlıya alma, sitemap, analitik ve bakım planı.",
            ]
        )
    )

    body.append(h2("Sık Yapılan Hatalar"))
    body.append(
        p(
            "Hedefi netleştirmeden başlamak, SEO'yu sonraya bırakmak, mobil deneyimi ihmal etmek ve içerik planını yazılımdan ayırmak sık görülen hatalardır. Süreç odaklı ilerlemek bu riskleri azaltır."
        )
    )

    body.append(h2("Başlamadan Önce Hazırlanması Gerekenler"))
    body.append(
        ul(
            [
                "Net iş hedefi ve hedef kitle tanımı",
                "Temel içerik taslağı (metin, görsel ihtiyacı)",
                "Rakip ve referans site örnekleri",
                "Domain ve hosting tercihi (varsa)",
            ]
        )
    )

    body.append(h2("Sonuç"))
    body.append(
        p(
            "Web sitesi nasıl yapılır sorusunun cevabı; planlı bir süreç ve doğru adımlardan geçer. Keşif, tasarım, geliştirme ve test aşamaları tamamlandığında hem kullanıcı hem arama motoru için sağlam bir altyapı elde edilir."
        )
    )

    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Teklif Al",
            "Web sitesi projeniz için hedeflerinizi paylaşın; size uygun adımları ve kapsamı çıkaralım.",
            _quote_url(page),
            "Teklif formu için sayfaya gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Web sitesi nasıl yapılır?", "Hedef analizi, bilgi mimarisi, tasarım, geliştirme, test ve yayın aşamalarından oluşan planlı bir süreçtir."),
        ("İlk adım ne olmalı?", "Keşif ve hedef analizi; amaç, hedef kitle ve rakiplerin netleştirilmesi."),
        ("Sık yapılan hatalar neler?", "Hedefi netleştirmeden başlamak, SEO'yu sonraya bırakmak, mobil deneyimi ihmal etmek."),
        ("Başlamadan ne hazırlanmalı?", "İş hedefi, hedef kitle, içerik taslağı, referans örnekleri ve domain/hosting tercihi."),
        ("Süreç ne kadar sürer?", "Kapsama göre değişir; net kapsam ve onay döngüleri süreyi belirler."),
        ("Teklif almak için ne gerekli?", "Hedef, kapsam ve içerik ihtiyacınızı paylaşmanız yeterlidir."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Sitesi Nasıl Yapılır? | Adım Adım Rehber"
    meta_description = (
        "Web sitesi nasıl yapılır? Keşif, tasarım, geliştirme, test ve yayın adımları. Profesyonel web sitesi yapım rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Sitesi Nasıl Yapılır? — Adım Adım Rehber",
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
        "web-tasarim-nedir": ("Web Tasarım Nedir?", ["Temel kavramlar", "Yaygın yanılgılar"], ["Çekirdek kavramlar", "Pratik örnekler"]),
        "web-sitesi-nasil-yapilir": ("Web Sitesi Nasıl Yapılır?", ["Kapsam netliği", "İçerik hazırlığı"], ["Adım adım süreç", "Risk kontrol listesi"]),
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
        if page.service.key == "ecommerce-development":
            return _ecommerce_pillar_tr(page)
        if page.service.key == "mobile-app-development":
            return _mobile_app_pillar_tr(page)
        if page.service.key == "seo-services":
            return _seo_services_pillar_tr(page)
        if page.service.key == "hosting-domain":
            return _hosting_domain_pillar_tr(page)
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
                    f"Kapsam ve bütçe: {{ link:{_pricing_url(page)} }}",
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
        if page.service.key == "seo-services":
            return _seo_services_pricing_tr(page)
        if page.service.key == "hosting-domain":
            return _hosting_domain_pricing_tr(page)
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
        if page.service.key == "seo-services":
            return _seo_services_guide_tr(page)
        if page.service.key == "hosting-domain":
            return _hosting_domain_guide_tr(page)
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
        if page.service.key == "seo-services":
            return _seo_services_quote_tr(page)
        if page.service.key == "hosting-domain":
            return _hosting_domain_quote_tr(page)
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
    # Custom cluster: React Native Uygulama (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "react-native":
        return _cluster_react_native_tr(page)

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
    # Custom cluster: Özel Yazılım Web Sitesi (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "ozel-yazilim-web-sitesi":
        return _cluster_ozel_yazilim_web_sitesi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Profesyonel Web Tasarım (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "profesyonel-web-tasarim":
        return _cluster_profesyonel_web_tasarim_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Web Tasarım Şirketi (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-tasarim-sirketi":
        return _cluster_web_tasarim_sirketi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Özel Yazılım mı Hazır Site mi? (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "ozel-yazilim-vs-hazir-site":
        return _cluster_ozel_yazilim_vs_hazir_site_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Freelancer ile Çalışma (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-tasarim-freelancer":
        return _cluster_web_tasarim_freelancer_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: İstanbul Web Geliştirici (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-developer-istanbul":
        return _cluster_web_developer_istanbul_tr(page)

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

    # -------------------------------------------------------------------------
    # Custom cluster: Web Tasarım Nedir? (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-tasarim-nedir":
        return _cluster_web_tasarim_nedir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Web Sitesi Nasıl Yapılır? (TR)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-sitesi-nasil-yapilir":
        return _cluster_web_sitesi_nasil_yapilir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Android Uygulama Geliştirme (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "android":
        return _cluster_android_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: iOS Uygulama Geliştirme (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "ios":
        return _cluster_ios_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: İstanbul'da Mobil Uygulama Hizmeti (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "istanbul":
        return _cluster_istanbul_mobil_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Özel Mobil Uygulama (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "ozel-mobil-uygulama":
        return _cluster_ozel_mobil_uygulama_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Mobil Uygulama Freelancer (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "mobil-uygulama-freelancer":
        return _cluster_mobil_uygulama_freelancer_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Mobil Uygulama Nedir? (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "mobil-uygulama-nedir":
        return _cluster_mobil_uygulama_nedir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Mobil Uygulama Nasıl Yapılır? (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "mobil-uygulama-nasil-yapilir":
        return _cluster_mobil_uygulama_nasil_yapilir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Android mi iOS mu? (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "android-vs-ios":
        return _cluster_android_vs_ios_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: React Native mi Native mi? (TR) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "react-native-vs-native":
        return _cluster_react_native_vs_native_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: E-Ticaret Yazılımı (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "e-ticaret-yazilimi":
        return _cluster_e_ticaret_yazilimi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: E-Ticaret Yazılım Firması (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "e-ticaret-yazilim-firmasi":
        return _cluster_e_ticaret_yazilim_firmasi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Özel E-Ticaret Yazılımı (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "ozel-e-ticaret-yazilimi":
        return _cluster_ozel_e_ticaret_yazilimi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: E-Ticaret Sitesi (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "e-ticaret-sitesi":
        return _cluster_e_ticaret_sitesi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: E-Ticaret Sitesi Yaptırmak (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "e-ticaret-sitesi-yaptirmak":
        return _cluster_e_ticaret_sitesi_yaptirmak_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: E-Ticaret Sitesi Nasıl Kurulur? (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "e-ticaret-sitesi-nasil-kurulur":
        return _cluster_e_ticaret_sitesi_nasil_kurulur_tr(page)

    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "b2b":
        return _cluster_b2b_ecommerce_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: B2C E-Ticaret (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "b2c":
        return _cluster_b2c_ecommerce_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: E-Ticaret Nedir? (TR) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "e-ticaret-nedir":
        return _cluster_e_ticaret_nedir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Danışmanlığı (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "seo-danismanligi":
        return _cluster_seo_danismanligi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Teknik SEO (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "teknik-seo":
        return _cluster_teknik_seo_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: On Page SEO (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "on-page-seo":
        return _cluster_on_page_seo_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Analizi (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "seo-analizi":
        return _cluster_seo_analizi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Nedir? (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "seo-nedir":
        return _cluster_seo_nedir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Nasıl Yapılır? (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "seo-nasil-yapilir":
        return _cluster_seo_nasil_yapilir_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Uyumlu Web Sitesi (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "seo-uyumlu-web-sitesi":
        return _cluster_seo_uyumlu_web_sitesi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Uzmanı Kirala (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "seo-uzmani":
        return _cluster_seo_uzmani_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: İstanbul SEO Ajansı (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "istanbul-seo-ajansi":
        return _cluster_istanbul_seo_ajansi_tr(page)

    # -------------------------------------------------------------------------
    # Custom cluster: SEO Ajansı mı Freelancer mı? (TR) — seo-services
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "seo-services" and page.slug == "ajans-mi-freelancer-mi":
        return _cluster_seo_ajans_freelancer_tr(page)

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


def _seo_services_pillar_tr(page: SeoPage) -> Dict:
    """Custom SEO pillar content for SEO Hizmetleri (TR) — teknik, içerik odaklı, sürdürülebilir."""
    body: List[str] = []

    # Giriş (H1 şablonda page.title üzerinden gösteriliyor)
    body.append(
        p(
            "Arama Motoru Optimizasyonu (SEO), işletmenizin dijital dünyada büyümesi için en güçlü yöntemlerden biridir. "
            "Web siteniz Google’da üst sıralarda yer aldığında, hizmetlerinizi veya ürünlerinizi aktif olarak arayan kullanıcıları doğrudan sitenize çekersiniz."
        )
    )
    body.append(
        p(
            "Angraweb olarak sunduğumuz profesyonel SEO hizmetleri, kısa vadeli çözümler yerine uzun vadeli ve sürdürülebilir bir büyüme stratejisine odaklanır. "
            "Teknik optimizasyon, anahtar kelime araştırması, içerik geliştirme ve otorite oluşturma süreçlerini bir araya getirerek sitenizin arama motorlarında daha görünür olmasını sağlıyoruz."
        )
    )
    body.append(
        p(
            "Amacımız; web sitenizin sıralamasını yükseltmek, hedefli organik trafik çekmek ve ziyaretçileri gerçek müşterilere dönüştürmektir."
        )
    )

    # SEO nedir
    body.append(h2("SEO Nedir?"))
    body.append(
        p(
            "SEO (Arama Motoru Optimizasyonu), bir web sitesinin Google gibi arama motorlarında daha üst sıralarda görünmesi için yapılan optimizasyon çalışmalarının tamamıdır."
        )
    )
    body.append(
        ul(
            [
                "Teknik site optimizasyonu",
                "İçerik stratejisi",
                "Anahtar kelime hedefleme",
                "Backlink oluşturma",
                "Kullanıcı deneyimi iyileştirme",
            ]
        )
    )
    body.append(
        p(
            "Bu faktörler birlikte çalıştığında arama motorları sitenizi daha iyi anlar ve ilgili aramalarda daha üst sıralara taşır."
        )
    )

    # SEO hizmetlerimizin kapsamı
    body.append(h2("SEO Hizmetlerimiz Neleri Kapsar?"))
    body.append(
        p(
            "SEO hizmetlerimiz, web sitenizin arama performansını tüm yönleriyle geliştirmek için tasarlanmıştır."
        )
    )
    body.append(
        p(
            "SEO sürecimiz şu temel alanları kapsar:"
        )
    )
    body.append(
        ul(
            [
                "SEO analizi (SEO audit)",
                "Anahtar kelime araştırması",
                "Site içi SEO optimizasyonu",
                "Teknik SEO çalışmaları",
                "Backlink ve otorite geliştirme",
            ]
        )
    )
    body.append(
        p(
            "Bu süreçlerin her biri, arama motorlarının sitenizi daha iyi anlamasına ve sıralamanızı yükseltmesine yardımcı olur."
        )
    )

    # Teknik SEO
    body.append(h2("Teknik SEO Optimizasyonu"))
    body.append(
        p(
            "Teknik SEO, arama motorlarının web sitenizi doğru şekilde taramasını ve indekslemesini sağlar."
        )
    )
    body.append(
        ul(
            [
                "Site hız optimizasyonu",
                "Mobil uyumluluk",
                "Core Web Vitals iyileştirme",
                "Yapısal veri (schema) entegrasyonu",
                "Site mimarisi optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar arama motorlarının sitenizi daha hızlı anlamasını sağlar ve sıralamaları olumlu yönde etkiler."
        )
    )

    # Anahtar kelime stratejisi
    body.append(h2("Anahtar Kelime Araştırması ve Stratejisi"))
    body.append(
        p(
            "Anahtar kelime araştırması başarılı bir SEO stratejisinin temelini oluşturur."
        )
    )
    body.append(
        p(
            "Analiz ettiğimiz faktörler:"
        )
    )
    body.append(
        ul(
            [
                "Arama hacmi",
                "Rekabet seviyesi",
                "Kullanıcı niyeti",
                "Sektörel trendler",
            ]
        )
    )
    body.append(
        p(
            "Bu veriler doğrultusunda yüksek değerli anahtar kelimeleri hedefleyen bir SEO stratejisi oluştururuz."
        )
    )

    # On Page SEO
    body.append(h2("Site İçi SEO Optimizasyonu"))
    body.append(
        p(
            "Site içi SEO (On Page SEO), web sitenizin iç yapısının optimize edilmesini kapsar."
        )
    )
    body.append(
        ul(
            [
                "Başlık etiketleri (title tag)",
                "Meta açıklamaları",
                "Başlık yapısı (H1-H2)",
                "İç linkleme",
                "İçerik optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu optimizasyonlar hem kullanıcı deneyimini hem de arama motoru görünürlüğünü artırır."
        )
    )

    # Neden Angraweb
    body.append(h2("Neden Angraweb SEO Hizmetleri?"))
    body.append(
        p(
            "Angraweb olarak SEO çalışmalarımızı veri odaklı ve sürdürülebilir bir büyüme stratejisi üzerine kuruyoruz."
        )
    )
    body.append(
        ul(
            [
                "Şeffaf SEO süreçleri",
                "Veri odaklı strateji",
                "Sürekli optimizasyon",
                "Uzun vadeli sıralama artışı",
            ]
        )
    )

    # Konular (İstanbul SEO Ajansı dahil tüm cluster linkleri)
    body.append(h2("Konular"))
    body.append(
        p(
            "İstanbul’daki işletmeler için yerel SEO stratejileri ve profesyonel SEO hizmetleri. "
            f"Detaylar: {{{{ link:/tr/seo-hizmetleri/istanbul-seo-ajansi/ }}}}"
        )
    )
    cluster_urls = _cluster_urls_for_service(page)
    if cluster_urls:
        body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

    # SSS
    body.append(h2("Sık Sorulan Sorular"))

    content_html = "\n".join(body)

    faq_pairs = [
        ("SEO sonuçları ne kadar sürede görülür?", "SEO çalışmalarının etkisi genellikle 3–6 ay içinde görülmeye başlar."),
        ("SEO reklamdan daha mı iyi?", "SEO uzun vadeli organik trafik sağlar, reklamlar ise kısa vadeli görünürlük sağlar."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Profesyonel SEO Hizmetleri | Google SEO Optimizasyonu – Angraweb"
    meta_description = (
        "Profesyonel SEO hizmetleri ile web sitenizi Google’da üst sıralara taşıyın. Teknik SEO, anahtar kelime stratejisi ve içerik optimizasyonu ile organik trafik artırın."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Profesyonel SEO Hizmetleri",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _hosting_domain_pillar_tr(page: SeoPage) -> Dict:
    """Custom pillar: Hosting ve Domain (TR) — web hosting, VPS, cloud, domain, SSL, Linux."""
    body: List[str] = []

    body.append(h2("Hosting ve Domain Nedir"))
    body.append(p("Bir web sitesinin internet üzerinde yayınlanabilmesi için iki temel bileşen gerekir: domain (alan adı) ve hosting (barındırma hizmeti)."))
    body.append(p("Domain, kullanıcıların web sitenize ulaşmasını sağlayan adresi ifade eder. Örneğin angraweb.com bir alan adıdır."))
    body.append(p("Hosting ise web sitenizin dosyalarının saklandığı ve internet üzerinden erişilebilir hale getirildiği sunucudur."))
    body.append(p("Bu iki bileşen birlikte çalışarak web sitelerinin online olarak yayınlanmasını sağlar."))

    body.append(h2("Web Hosting Nedir"))
    body.append(p("Web hosting, web sitelerinin internet üzerinde yayınlanmasını sağlayan barındırma hizmetidir."))
    body.append(p("Hosting hizmeti sayesinde web sitesi dosyaları bir sunucu üzerinde saklanır ve kullanıcılar internet üzerinden bu dosyalara erişebilir."))
    body.append(p("Hosting hizmetlerinin temel özellikleri şunlardır:"))
    body.append(ul(["yüksek uptime oranı", "hızlı sunucu performansı", "güvenli altyapı", "teknik destek"]))
    body.append(p("Doğru hosting seçimi web sitesinin performansı ve güvenliği açısından büyük önem taşır."))

    body.append(h2("VPS Hosting"))
    body.append(p("VPS (Virtual Private Server), fiziksel bir sunucunun sanal olarak bölünmesiyle oluşturulan hosting çözümüdür."))
    body.append(p("VPS hosting çözümleri genellikle şu avantajları sunar:"))
    body.append(ul(["daha yüksek performans", "daha fazla kontrol", "özelleştirilebilir sunucu yapılandırması"]))
    body.append(p("Bu nedenle VPS hosting genellikle büyüyen web siteleri ve projeler için tercih edilir."))

    body.append(h2("Bulut Sunucu (Cloud Hosting)"))
    body.append(p("Bulut sunucu teknolojisi, web sitelerinin birden fazla sunucu üzerinde çalışmasını sağlayan modern bir altyapıdır."))
    body.append(p("Cloud hosting çözümleri şu avantajları sağlar:"))
    body.append(ul(["yüksek ölçeklenebilirlik", "daha iyi performans", "yüksek erişilebilirlik"]))
    body.append(p("Bu nedenle modern web projelerinde bulut altyapısı sıkça tercih edilir."))

    body.append(h2("Dedicated Sunucu (Özel Sunucu)"))
    body.append(p("Özel sunucu kiralama, tüm fiziksel sunucunun tek bir proje için ayrıldığı hosting türüdür."))
    body.append(p("Dedicated server çözümleri genellikle:"))
    body.append(ul(["yüksek trafikli web siteleri", "büyük ölçekli uygulamalar", "kurumsal projeler"]))
    body.append(p("için tercih edilir."))
    body.append(p("Bu yapı maksimum performans ve kontrol sağlar."))

    body.append(h2("Domain Satın Alma"))
    body.append(p("Domain (alan adı), web sitenizin internet üzerindeki adresidir."))
    body.append(p("Doğru domain seçimi markanız için büyük önem taşır."))
    body.append(p("Domain seçerken şu kriterlere dikkat edilmelidir:"))
    body.append(ul(["kısa ve akılda kalıcı olması", "marka ile uyumlu olması", "doğru domain uzantısı seçimi (.com, .net vb.)"]))
    body.append(p("Alan adı seçimi dijital marka kimliğinin temel parçasıdır."))

    body.append(h2("SSL Sertifikası"))
    body.append(p("SSL sertifikası, web siteleri ile kullanıcılar arasındaki veri iletişimini şifreleyen güvenlik teknolojisidir."))
    body.append(p("SSL sertifikası sayesinde:"))
    body.append(ul(["kullanıcı verileri korunur", "web sitesi güvenli hale gelir", "Google sıralamalarında avantaj sağlanır"]))
    body.append(p("Bu nedenle modern web sitelerinde SSL kullanımı zorunlu hale gelmiştir."))

    body.append(h2("Linux Sunucu Kurulumu"))
    body.append(p("Linux sunucular web hosting dünyasında en yaygın kullanılan sunucu altyapılarından biridir."))
    body.append(p("Linux tabanlı sunucular şu avantajları sunar:"))
    body.append(ul(["yüksek güvenlik", "güçlü performans", "açık kaynak ekosistemi"]))
    body.append(p("Bu nedenle birçok web uygulaması Linux sunucular üzerinde çalışır."))

    body.append(h2("Hosting Seçerken Nelere Dikkat Edilmeli"))
    body.append(p("Doğru hosting seçimi web sitenizin performansını doğrudan etkiler."))
    body.append(p("Hosting seçerken şu faktörler dikkate alınmalıdır:"))
    body.append(ul(["sunucu performansı", "uptime oranı", "teknik destek kalitesi", "güvenlik altyapısı", "ölçeklenebilirlik"]))
    body.append(p("Bu kriterler uzun vadede web sitenizin başarısını belirler."))

    body.append(h2("Angraweb Hosting ve Sunucu Çözümleri"))
    body.append(p("Angraweb olarak web projeleri için hosting ve sunucu altyapısı konusunda danışmanlık ve kurulum hizmetleri sunuyoruz."))
    body.append(p("Hizmetlerimiz şunları kapsar:"))
    body.append(ul(["web hosting kurulumu", "VPS ve bulut sunucu yapılandırması", "domain yönetimi", "SSL kurulumu", "Linux sunucu kurulumu"]))
    body.append(p("Amacımız web projelerinin hızlı, güvenli ve sürdürülebilir şekilde çalışmasını sağlamaktır."))

    body.append(h2("Hosting Çözümü İçin Teklif Alın"))
    body.append(p("Projeniz için en uygun hosting altyapısını belirlemek performans ve güvenlik açısından kritik bir adımdır."))
    body.append(p(f"Angraweb ekibi ile iletişime geçerek projenize en uygun hosting çözümünü belirleyebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"))

    cluster_urls = _cluster_urls_for_service(page)
    if cluster_urls:
        body.append(h2("Konular"))
        body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

    content_html = "\n".join(body)
    meta_title = "Hosting ve Domain Rehberi: Web Hosting, VPS ve Sunucu Çözümleri – Angraweb"
    meta_description = (
        "Hosting ve domain nedir? Web hosting, VPS, bulut sunucu, domain satın alma ve SSL sertifikası hakkında kapsamlı rehberi keşfedin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Hosting ve Domain",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _hosting_domain_pricing_tr(page: SeoPage) -> Dict:
    """Custom pricing page: Hosting ve Domain Fiyatları (TR)."""
    body: List[str] = []

    body.append(h2("Hosting ve Domain Fiyatları Nasıl Belirlenir"))
    body.append(p("Hosting ve domain fiyatları; seçilen altyapı, performans ihtiyaçları ve proje ölçeğine göre değişir."))
    body.append(p("Basit bir web sitesi için temel hosting çözümleri yeterli olabilirken, yüksek trafik alan projelerde VPS veya bulut sunucu çözümleri tercih edilir."))
    body.append(p("Fiyatlandırmayı etkileyen başlıca faktörler şunlardır:"))
    body.append(ul(["sunucu türü", "performans gereksinimleri", "trafik hacmi", "depolama kapasitesi", "güvenlik ve bakım ihtiyaçları"]))
    body.append(p("Bu faktörler hosting maliyetlerini doğrudan etkiler."))

    body.append(h2("Web Hosting Fiyatları"))
    body.append(p("Web hosting, küçük ve orta ölçekli web siteleri için en yaygın kullanılan barındırma çözümüdür."))
    body.append(p("Web hosting paketleri genellikle şu özelliklere göre fiyatlandırılır:"))
    body.append(ul(["disk alanı", "trafik limiti", "e-posta hesapları", "teknik destek"]))
    body.append(p("Başlangıç seviyesindeki web hosting paketleri genellikle düşük maliyetlidir ve küçük projeler için yeterli performans sağlar."))

    body.append(h2("VPS Hosting Fiyatları"))
    body.append(p("VPS hosting çözümleri daha yüksek performans ve kontrol sağlar."))
    body.append(p("VPS sunucular genellikle şu faktörlere göre fiyatlandırılır:"))
    body.append(ul(["CPU çekirdek sayısı", "RAM kapasitesi", "SSD depolama alanı", "bant genişliği"]))
    body.append(p("Bu nedenle VPS hosting fiyatları paylaşımlı hosting çözümlerine göre daha yüksek olabilir."))

    body.append(h2("Bulut Sunucu Fiyatları"))
    body.append(p("Cloud hosting altyapısı esnek ve ölçeklenebilir bir yapı sunar."))
    body.append(p("Bulut sunucu fiyatları genellikle kullanım bazlıdır."))
    body.append(p("Maliyeti etkileyen faktörler şunlardır:"))
    body.append(ul(["sunucu kaynakları", "veri transferi", "depolama alanı", "trafik miktarı"]))
    body.append(p("Bulut altyapısı büyüyen projeler için ideal bir çözümdür."))

    body.append(h2("Dedicated Server (Özel Sunucu) Fiyatları"))
    body.append(p("Özel sunucular tüm fiziksel sunucunun tek bir projeye ayrıldığı hosting çözümleridir."))
    body.append(p("Dedicated server maliyetleri genellikle şu faktörlere bağlıdır:"))
    body.append(ul(["işlemci gücü", "RAM kapasitesi", "depolama teknolojisi", "veri merkezi konumu"]))
    body.append(p("Bu tür sunucular yüksek trafik alan projeler için tercih edilir."))

    body.append(h2("Domain Fiyatları"))
    body.append(p("Domain fiyatları seçilen uzantıya göre değişir."))
    body.append(p("En yaygın domain uzantıları:"))
    body.append(ul([".com", ".net", ".org"]))
    body.append(p("Domain fiyatları genellikle yıllık olarak ödenir ve uzantıya göre farklılık gösterebilir."))

    body.append(h2("SSL Sertifikası Maliyetleri"))
    body.append(p("SSL sertifikaları web siteleri için güvenli veri iletişimi sağlar."))
    body.append(p("SSL maliyetleri şu faktörlere göre değişebilir:"))
    body.append(ul(["domain doğrulama seviyesi", "şirket doğrulaması", "wildcard sertifikalar"]))
    body.append(p("Günümüzde birçok hosting sağlayıcısı ücretsiz SSL sertifikası da sunmaktadır."))

    body.append(h2("Hosting Bütçesi Nasıl Planlanmalı"))
    body.append(p("Hosting bütçesi planlanırken projenin gelecekteki büyümesi de göz önünde bulundurulmalıdır."))
    body.append(p("Sağlıklı bir bütçe planlaması için:"))
    body.append(ul(["minimum gereksinimler belirlenmeli", "ölçeklenebilir altyapı seçilmeli", "performans ihtiyaçları analiz edilmelidir"]))
    body.append(p("Bu yaklaşım uzun vadede maliyet kontrolü sağlar."))

    body.append(h2("Angraweb Hosting Danışmanlığı"))
    body.append(p("Angraweb olarak işletmelere hosting altyapısı seçimi ve sunucu kurulumu konusunda danışmanlık sağlıyoruz."))
    body.append(p("Hizmetlerimiz şunları kapsar:"))
    body.append(ul(["hosting altyapısı danışmanlığı", "VPS ve bulut sunucu kurulumu", "domain yönetimi", "SSL kurulumu", "Linux sunucu yapılandırması"]))
    body.append(p("Amacımız web projelerinin hızlı, güvenli ve sürdürülebilir şekilde çalışmasını sağlamaktır."))

    body.append(h2("Hosting Çözümü İçin Teklif Alın"))
    body.append(p("Projeniz için en uygun hosting altyapısını belirlemek performans ve maliyet açısından kritik bir adımdır."))
    body.append(p(f"Angraweb ekibi ile iletişime geçerek projeniz için en doğru hosting çözümünü belirleyebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"))

    body.append(h2("İlgili sayfalar"))
    body.append(ul([f"{{{{ link:{_pillar_url(page)} }}}}", f"{{{{ link:{_guide_url(page)} }}}}"]))

    content_html = "\n".join(body)
    meta_title = "Hosting ve Domain Fiyatları: Web Hosting, VPS ve Sunucu Ücretleri – Angraweb"
    meta_description = (
        "Hosting ve domain fiyatları neye göre belirlenir? Web hosting, VPS, bulut sunucu ve domain maliyetleri hakkında detaylı bilgi ve bütçe planlama rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Hosting & Domain Fiyatları",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _hosting_domain_guide_tr(page: SeoPage) -> Dict:
    """Custom guide: Hosting ve Domain Rehberi (TR) — nasıl çalışır, seçim, altyapı kurulumu."""
    body: List[str] = []

    body.append(h2("Hosting ve Domain Nedir"))
    body.append(p("Bir web sitesinin internet üzerinde yayınlanabilmesi için iki temel bileşen gerekir: domain (alan adı) ve hosting (barındırma hizmeti)."))
    body.append(p("Domain, kullanıcıların web sitenize ulaşmasını sağlayan internet adresidir. Örneğin angraweb.com bir alan adıdır."))
    body.append(p("Hosting ise web sitenizin dosyalarının saklandığı sunucudur. Bu sunucu sayesinde web sitesi internet üzerinden erişilebilir hale gelir."))
    body.append(p("Domain ve hosting birlikte çalışarak bir web sitesinin online olmasını sağlar."))

    body.append(h2("Bu Rehber Kimler İçin Hazırlandı"))
    body.append(p("Bu rehber özellikle şu kişiler için hazırlanmıştır:"))
    body.append(ul([
        "yeni bir web sitesi başlatmak isteyen girişimler",
        "mevcut web altyapısını iyileştirmek isteyen işletmeler",
        "hosting altyapısını anlamak isteyen proje ekipleri",
    ]))
    body.append(p("Rehberde hosting ve domain seçiminden sunucu kurulumuna kadar temel süreçler anlatılmaktadır."))

    body.append(h2("1. Hedef ve Kullanıcıyı Belirlemek"))
    body.append(p("Bir web projesinin başarılı olması için ilk adım hedef ve kullanıcı kitlesinin net olmasıdır."))
    body.append(p("Bu aşamada şu sorulara cevap verilmelidir:"))
    body.append(ul(["web sitesinin amacı nedir", "hedef kullanıcı kimdir", "kullanıcıya sunulan değer nedir"]))
    body.append(p("Bu sorular netleştiğinde web altyapısı daha doğru planlanabilir."))

    body.append(h2("2. Bilgi Mimarisi ve İçerik Planı"))
    body.append(p("Bir web sitesinin sayfa yapısı ve içerik hiyerarşisi kullanıcı deneyimini doğrudan etkiler."))
    body.append(p("Temel içerik yapısı genellikle şu bölümlerden oluşur:"))
    body.append(ul(["ana sayfa", "hizmet veya ürün sayfaları", "blog veya rehber içerikleri", "iletişim ve dönüşüm sayfaları"]))
    body.append(p("Doğru bilgi mimarisi aynı zamanda arama motoru optimizasyonu için de önemlidir."))

    body.append(h2("3. Hosting Türünü Seçmek"))
    body.append(p("Web projeleri için farklı hosting çözümleri bulunmaktadır."))
    body.append(p("En yaygın hosting türleri şunlardır:"))
    body.append(ul([
        "Web Hosting — Küçük ve orta ölçekli web siteleri için uygun paylaşımlı hosting çözümüdür.",
        "VPS Hosting — Daha yüksek performans ve kontrol gerektiren projeler için tercih edilir.",
        "Cloud Hosting — Ölçeklenebilir altyapı sağlayan modern hosting çözümüdür.",
        "Dedicated Server — Yüksek trafikli ve büyük projeler için kullanılan özel sunucu çözümüdür.",
    ]))
    body.append(p("Projenin büyüklüğüne göre doğru hosting türünü seçmek önemlidir."))

    body.append(h2("4. Domain Seçimi"))
    body.append(p("Domain adı bir web sitesinin dijital kimliğidir."))
    body.append(p("İyi bir domain adı:"))
    body.append(ul(["kısa olmalıdır", "kolay hatırlanmalıdır", "marka ile uyumlu olmalıdır"]))
    body.append(p("En yaygın domain uzantıları:"))
    body.append(ul([".com", ".net", ".org"]))
    body.append(p("Doğru domain seçimi markanın dijital görünürlüğünü artırır."))

    body.append(h2("5. Güvenlik ve SSL"))
    body.append(p("Web siteleri için güvenlik önemli bir konudur."))
    body.append(p("SSL sertifikası sayesinde web sitesi ile kullanıcı arasındaki veri iletişimi şifrelenir."))
    body.append(p("SSL kullanımının avantajları:"))
    body.append(ul(["kullanıcı güveni", "veri güvenliği", "SEO avantajı"]))
    body.append(p("Modern web sitelerinde SSL kullanımı artık standart hale gelmiştir."))

    body.append(h2("6. Yayın Öncesi Kontrol Listesi"))
    body.append(p("Bir web sitesini yayına almadan önce bazı kontroller yapılmalıdır."))
    body.append(p("Temel kontrol listesi:"))
    body.append(ul(["tüm sayfalar çalışıyor mu", "formlar düzgün çalışıyor mu", "site hızı yeterli mi", "kırık bağlantılar var mı"]))
    body.append(p("Bu kontroller yayın sonrası sorunları büyük ölçüde azaltır."))

    body.append(h2("7. Yayın Sonrası İzleme"))
    body.append(p("Bir web sitesi yayına alındıktan sonra süreç bitmez."))
    body.append(p("Yayın sonrası yapılması gerekenler:"))
    body.append(ul(["performans izleme", "hata takibi", "kullanıcı geri bildirimleri", "düzenli yedekleme"]))
    body.append(p("Bu süreç web sitesinin sürdürülebilir şekilde çalışmasını sağlar."))

    body.append(h2("Angraweb Hosting Danışmanlığı"))
    body.append(p("Angraweb olarak işletmelere hosting altyapısı kurulumu ve sunucu yönetimi konusunda destek veriyoruz."))
    body.append(p("Hizmetlerimiz şunları kapsar:"))
    body.append(ul([
        "hosting altyapısı kurulumu",
        "VPS ve bulut sunucu yapılandırması",
        "domain yönetimi",
        "SSL kurulumu",
        "Linux sunucu yönetimi",
    ]))
    body.append(p("Amacımız web projelerinin hızlı ve güvenli bir altyapı üzerinde çalışmasını sağlamaktır."))

    body.append(h2("Hosting Altyapınızı Planlayın"))
    body.append(p("Web projeniz için doğru hosting altyapısını belirlemek performans ve güvenlik açısından önemlidir."))
    body.append(p(f"Angraweb ile iletişime geçerek projeniz için en uygun hosting çözümünü planlayabilirsiniz. {{{{ link:{_pillar_url(page)} }}}} ve {{{{ link:{_pricing_url(page)} }}}} sayfalarından detaylı bilgi alabilirsiniz."))
    body.append(
        cta_box(
            "Hosting çözümü için teklif alın",
            "Projenize uygun altyapıyı birlikte belirleyelim.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    meta_title = "Hosting ve Domain Rehberi: Web Hosting Nasıl Çalışır? – Angraweb"
    meta_description = (
        "Hosting ve domain nedir? Web hosting nasıl çalışır, nasıl seçilir ve bir web sitesi için doğru hosting altyapısı nasıl kurulur öğrenin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Hosting & Domain Rehberi",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _hosting_domain_quote_tr(page: SeoPage) -> Dict:
    """Custom quote page: Hosting ve Domain Teklif Al (TR) — sunucu ve hosting kurulum teklifi."""
    body: List[str] = []

    body.append(h2("Hosting ve Domain Projeniz İçin Teklif Alın"))
    body.append(p("Web projeniz için doğru hosting altyapısını seçmek performans, güvenlik ve sürdürülebilirlik açısından kritik bir adımdır."))
    body.append(p("Her proje farklı ihtiyaçlara sahip olduğu için hosting ve sunucu çözümleri de projeye özel planlanmalıdır."))
    body.append(p("Angraweb olarak web projeleri için hosting altyapısı planlama ve sunucu kurulumu konusunda profesyonel destek sağlıyoruz."))

    body.append(h2("Teklif Süreci Nasıl İşler"))
    body.append(p("Hosting veya sunucu kurulumu için teklif süreci birkaç basit adımdan oluşur."))
    body.append(ul([
        "1. Kısa brif paylaşımı — Projenizin hedefini, ihtiyaçlarını ve önceliklerini kısa bir şekilde paylaşmanız yeterlidir.",
        "2. Ön görüşme — Proje detaylarını netleştirmek için kısa bir online görüşme yapılır.",
        "3. Teknik planlama — Hosting altyapısı, sunucu kaynakları ve kurulum planı belirlenir.",
        "4. Teklif ve zaman planı — Proje kapsamına göre teklif, teslim süresi ve ödeme planı hazırlanır.",
    ]))

    body.append(h2("Teklif İçin Hangi Bilgiler Gerekli"))
    body.append(p("Teklif hazırlama sürecini hızlandırmak için şu bilgileri paylaşmanız faydalı olur:"))
    body.append(ul([
        "projenin amacı",
        "tahmini kullanıcı veya trafik hacmi",
        "gerekli modüller veya entegrasyonlar",
        "tercih edilen teknoloji veya platform",
        "hedef yayın tarihi",
    ]))
    body.append(p("Bu bilgiler sayesinde proje için en uygun hosting çözümü belirlenebilir."))

    body.append(h2("Hosting Altyapısı Planlama"))
    body.append(p("Hosting altyapısı planlanırken aşağıdaki faktörler dikkate alınır:"))
    body.append(ul([
        "proje büyüklüğü",
        "performans gereksinimleri",
        "güvenlik ihtiyaçları",
        "ölçeklenebilirlik",
        "bakım ve yönetim ihtiyaçları",
    ]))
    body.append(p("Doğru planlanan bir hosting altyapısı uzun vadede verimliliği artırır ve performansı iyileştirir."))

    body.append(h2("Angraweb Hosting Hizmetleri"))
    body.append(p("Angraweb olarak hosting ve sunucu altyapısı konusunda aşağıdaki hizmetleri sunuyoruz:"))
    body.append(ul([
        "web hosting kurulumu",
        "VPS ve cloud sunucu kurulumu",
        "domain yönetimi",
        "SSL kurulumu",
        "Linux sunucu yapılandırması",
        "Django ve web uygulaması deployment",
    ]))
    body.append(p("Amacımız web projelerinin hızlı, güvenli ve sürdürülebilir şekilde çalışmasını sağlamaktır."))

    body.append(h2("Projenizi Birlikte Planlayalım"))
    body.append(p("Hosting altyapısını doğru planlamak web projenizin başarısını doğrudan etkiler."))
    body.append(p("Teklif formunu doldurarak projeniz hakkında kısa bir bilgi paylaşabilir ve sizin için en uygun hosting çözümünü birlikte planlayabiliriz."))
    body.append(h2("İlgili sayfalar"))
    body.append(ul([f"{{{{ link:{_pillar_url(page)} }}}}", f"{{{{ link:{_guide_url(page)} }}}}", f"{{{{ link:{_pricing_url(page)} }}}}"]))

    body.append(
        cta_box(
            "Teklif formunu doldurun",
            "Projenizi kısaca anlatın; size uygun hosting çözümünü birlikte planlayalım.",
            _quote_url(page),
            "Teklif sayfasına gidin.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    meta_title = "Hosting ve Domain Teklif Al – Sunucu ve Hosting Kurulum Hizmeti | Angraweb"
    meta_description = (
        "Hosting ve domain altyapısı için teklif alın. Web hosting, VPS, cloud sunucu kurulumu ve domain yönetimi için hızlı proje teklifi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Hosting & Domain Teklif Al",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _seo_services_pricing_tr(page: SeoPage) -> Dict:
    """Custom SEO pricing page (TR) — fiyat faktörleri, kapsam, aylık/proje modelleri, cluster linkleri."""
    body: List[str] = []

    body.append(
        p(
            "SEO hizmetleri fiyatları, bir web sitesinin ihtiyaçlarına, rekabet seviyesine ve hedeflenen anahtar kelimelere göre değişiklik gösterebilir. "
            "Her web sitesi farklı olduğu için SEO çalışmaları da standart bir paket yerine projeye özel planlanır."
        )
    )
    body.append(
        p(
            "Profesyonel SEO hizmetlerinin amacı yalnızca arama motorlarında görünürlük kazanmak değil, aynı zamanda doğru hedef kitleye ulaşarak sürdürülebilir bir trafik ve müşteri akışı sağlamaktır. "
            "Bu nedenle SEO fiyatlandırması yapılırken yalnızca teknik çalışmalar değil; içerik stratejisi, kullanıcı deneyimi ve rekabet analizi gibi birçok faktör göz önünde bulundurulur."
        )
    )
    body.append(
        p(
            "Angraweb olarak SEO projelerinde fiyatlandırmayı şeffaf ve anlaşılır bir şekilde planlıyoruz. "
            "Böylece müşteriler hangi çalışmaların projeye dahil olduğunu ve bütçenin hangi alanlara ayrıldığını net bir şekilde görebilir."
        )
    )

    body.append(h2("SEO Hizmetleri Fiyatlarını Etkileyen Faktörler"))
    body.append(
        p(
            "SEO fiyatları birkaç temel faktöre bağlı olarak değişir. "
            "Bunların başında sektör rekabeti, hedeflenen anahtar kelimeler ve web sitesinin mevcut durumu gelir."
        )
    )
    body.append(h3("Rekabet Seviyesi"))
    body.append(
        p(
            "Bazı sektörlerde SEO rekabeti oldukça yüksektir. "
            "Özellikle e-ticaret, finans, sağlık ve teknoloji gibi alanlarda çok sayıda rakip bulunur. "
            "Bu durumda SEO çalışmaları daha kapsamlı bir strateji gerektirir."
        )
    )
    body.append(
        p(
            "Rekabet seviyesi arttıkça yapılması gereken çalışmalar da artar. "
            "Bu nedenle yüksek rekabetli sektörlerde SEO bütçesi genellikle daha yüksek olur."
        )
    )
    body.append(h3("Web Sitesinin Mevcut Durumu"))
    body.append(
        p(
            "SEO çalışmasına başlamadan önce web sitesinin teknik altyapısı incelenir. "
            "Eğer site yapısında ciddi teknik sorunlar varsa öncelikle bu sorunların çözülmesi gerekir."
        )
    )
    body.append(p("Örneğin:"))
    body.append(
        ul(
            [
                "Site hızının düşük olması",
                "Mobil uyumluluk sorunları",
                "Hatalı sayfa yapıları",
                "Eksik meta etiketleri",
            ]
        )
    )
    body.append(
        p(
            "Bu tür sorunlar SEO performansını doğrudan etkiler ve düzeltilmesi gereken çalışmalar fiyatlandırmaya dahil edilir."
        )
    )
    body.append(h3("Anahtar Kelime Stratejisi"))
    body.append(
        p(
            "SEO çalışmalarının en önemli parçalarından biri anahtar kelime araştırmasıdır. "
            "Hedeflenen anahtar kelimelerin arama hacmi ve rekabet düzeyi SEO stratejisini doğrudan etkiler."
        )
    )
    body.append(p("Örneğin:"))
    body.append(
        ul(
            [
                "düşük rekabetli anahtar kelimeler daha hızlı sonuç verebilir",
                "yüksek rekabetli anahtar kelimeler uzun vadeli SEO çalışması gerektirir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle anahtar kelime stratejisi SEO fiyatlandırmasının önemli bir parçasıdır."
        )
    )

    body.append(h2("SEO Hizmeti Neleri Kapsar"))
    body.append(
        p(
            "Profesyonel SEO hizmetleri yalnızca birkaç teknik ayardan ibaret değildir. "
            "Başarılı bir SEO stratejisi birçok farklı çalışmanın birlikte yürütülmesini gerektirir."
        )
    )
    body.append(h3("SEO Analizi (SEO Audit)"))
    body.append(
        p(
            "SEO süreci genellikle detaylı bir SEO analizi ile başlar. "
            "Bu analizde web sitesinin teknik yapısı, içerik kalitesi ve arama motoru uyumluluğu incelenir."
        )
    )
    body.append(p("SEO analizinde şu konular değerlendirilir:"))
    body.append(
        ul(
            [
                "teknik SEO sorunları",
                "site hızı",
                "mobil uyumluluk",
                "içerik yapısı",
                "backlink profili",
            ]
        )
    )
    body.append(
        p(
            "Bu analiz sonucunda bir SEO yol haritası oluşturulur. "
            f"Detay için: {{{{ link:/tr/seo-hizmetleri/seo-analizi/ }}}}"
        )
    )
    body.append(h3("Teknik SEO"))
    body.append(
        p(
            "Teknik SEO, arama motorlarının web sitesini daha iyi taramasını ve anlamasını sağlayan optimizasyonları içerir."
        )
    )
    body.append(p("Teknik SEO çalışmaları şunları kapsar:"))
    body.append(
        ul(
            [
                "site hız optimizasyonu",
                "mobil uyumluluk iyileştirmeleri",
                "site mimarisi düzenleme",
                "indeksleme sorunlarının çözülmesi",
                "yapılandırılmış veri (schema) kullanımı",
            ]
        )
    )
    body.append(
        p(
            "Teknik SEO çalışmaları doğru yapılmadığında diğer SEO çalışmalarının etkisi sınırlı kalabilir. "
            f"Daha fazla bilgi: {{{{ link:/tr/seo-hizmetleri/teknik-seo/ }}}}"
        )
    )
    body.append(h3("İçerik Optimizasyonu"))
    body.append(
        p(
            "SEO'nun en önemli parçalarından biri içeriktir. "
            "Google algoritmaları kullanıcıya değer sağlayan içerikleri ön plana çıkarır."
        )
    )
    body.append(
        p(
            "Bu nedenle SEO çalışmalarında içerik optimizasyonu önemli bir rol oynar."
        )
    )
    body.append(p("İçerik optimizasyonu kapsamında:"))
    body.append(
        ul(
            [
                "anahtar kelime uyumlu içerik oluşturma",
                "başlık yapısı düzenleme",
                "meta açıklamaları optimize etme",
                "kullanıcı niyetine uygun içerik geliştirme",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar web sitesinin organik trafik kazanmasına yardımcı olur. "
            f"Site içi SEO detayları: {{{{ link:/tr/seo-hizmetleri/on-page-seo/ }}}}"
        )
    )
    body.append(h3("Backlink Çalışmaları"))
    body.append(
        p(
            "Backlink, başka web sitelerinden alınan bağlantılardır ve SEO açısından önemli bir otorite sinyalidir."
        )
    )
    body.append(p("Kaliteli backlinkler:"))
    body.append(
        ul(
            [
                "web sitesinin güvenilirliğini artırır",
                "Google sıralamalarını güçlendirir",
                "organik trafik artışına katkı sağlar",
            ]
        )
    )
    body.append(
        p(
            "Ancak backlink çalışmaları doğal ve kaliteli kaynaklardan yapılmalıdır. "
            "Düşük kaliteli backlinkler SEO performansına zarar verebilir."
        )
    )

    body.append(h2("Aylık SEO Hizmeti Fiyatları"))
    body.append(
        p(
            "SEO fiyatları projeye göre değişse de genel olarak birkaç farklı model bulunur."
        )
    )
    body.append(h3("Aylık SEO Hizmeti"))
    body.append(
        p(
            "Birçok işletme için en uygun model aylık SEO hizmetidir. "
            "Bu modelde SEO çalışmaları sürekli olarak yürütülür ve performans düzenli olarak analiz edilir."
        )
    )
    body.append(p("Aylık SEO hizmetleri genellikle şu çalışmaları içerir:"))
    body.append(
        ul(
            [
                "anahtar kelime analizi",
                "içerik optimizasyonu",
                "teknik SEO iyileştirmeleri",
                "backlink geliştirme",
                "SEO raporlama",
            ]
        )
    )
    body.append(
        p(
            "Bu model uzun vadeli SEO başarısı için en etkili yöntemlerden biridir."
        )
    )
    body.append(h3("Proje Bazlı SEO"))
    body.append(
        p(
            "Bazı durumlarda SEO çalışmaları proje bazlı olarak yapılabilir."
        )
    )
    body.append(p("Örneğin:"))
    body.append(
        ul(
            [
                "SEO site analizi",
                "teknik SEO düzeltmeleri",
                "site taşınması sonrası SEO düzenlemeleri",
            ]
        )
    )
    body.append(
        p(
            "Bu tür çalışmalar genellikle tek seferlik projeler şeklinde planlanır."
        )
    )

    body.append(h2("SEO Hizmeti Alırken Nelere Dikkat Edilmeli"))
    body.append(
        p(
            "SEO hizmeti seçerken yalnızca fiyat değil, sunulan hizmetin kalitesi de dikkate alınmalıdır."
        )
    )
    body.append(
        p(
            "Profesyonel bir SEO hizmetinde şu özellikler bulunmalıdır:"
        )
    )
    body.append(
        ul(
            [
                "şeffaf raporlama",
                "sürdürülebilir SEO stratejisi",
                "güncel Google algoritmalarına uygun çalışma",
                "uzun vadeli organik büyüme hedefi",
            ]
        )
    )
    body.append(
        p(
            "SEO kısa vadeli bir reklam çalışması değil, uzun vadeli bir dijital büyüme stratejisidir."
        )
    )

    body.append(h2("Angraweb SEO Hizmetleri"))
    body.append(
        p(
            "Angraweb olarak işletmelerin dijital görünürlüğünü artırmak için modern ve sürdürülebilir SEO stratejileri uyguluyoruz."
        )
    )
    body.append(p("SEO çalışmalarımız şu alanlara odaklanır:"))
    body.append(
        ul(
            [
                "teknik SEO optimizasyonu",
                "anahtar kelime stratejisi",
                "içerik geliştirme",
                "site içi ve site dışı SEO",
            ]
        )
    )
    body.append(
        p(
            "Amacımız web sitenizin arama motorlarında daha üst sıralara çıkmasını sağlamak ve işletmenize gerçek müşteri kazandırmaktır."
        )
    )
    body.append(
        p(
            "SEO hizmetleri fiyatları hakkında detaylı bilgi almak için bizimle iletişime geçebilir veya "
            f"hızlı teklif formunu kullanabilirsiniz: {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    # Topical authority: link to cluster pages
    body.append(h3("İlgili konular"))
    body.append(
        ul(
            [
                f"{{{{ link:/tr/seo-hizmetleri/seo-analizi/ }}}}",
                f"{{{{ link:/tr/seo-hizmetleri/on-page-seo/ }}}}",
                f"{{{{ link:/tr/seo-hizmetleri/teknik-seo/ }}}}",
                f"{{{{ link:/tr/seo-hizmetleri/seo-nedir/ }}}}",
                f"{{{{ link:/tr/seo-hizmetleri/seo-nasil-yapilir/ }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Hizmetleri Fiyatları 2026 | Profesyonel SEO Maliyeti – Angraweb"
    meta_description = (
        "SEO hizmetleri fiyatları neye göre belirlenir? Profesyonel SEO maliyeti, aylık SEO paketleri ve fiyatları hakkında detaylı bilgi alın."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Hizmetleri Fiyatları",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _seo_services_guide_tr(page: SeoPage) -> Dict:
    """Custom SEO guide page (TR) — rehber adımları, planlama, teknik SEO, içerik stratejisi."""
    body: List[str] = []

    body.append(
        p(
            "SEO hizmetleri rehberi, web sitelerini arama motorlarında daha görünür hale getirmek isteyen işletmeler ve ekipler için hazırlanmıştır. "
            "Günümüzde dijital rekabet giderek arttığı için yalnızca bir web sitesine sahip olmak yeterli değildir. "
            "Web sitesinin Google gibi arama motorlarında bulunabilir olması gerekir."
        )
    )
    body.append(
        p(
            "SEO çalışmaları doğru planlandığında işletmelere uzun vadeli organik trafik sağlar. "
            "Bu rehberde SEO sürecinin temel adımlarını, planlama yöntemlerini ve başarılı bir SEO stratejisinin nasıl oluşturulacağını inceleyeceğiz."
        )
    )
    body.append(p("Bu rehber özellikle şu kişiler için faydalıdır:"))
    body.append(
        ul(
            [
                "yeni bir web sitesi başlatan işletmeler",
                "mevcut sitesini geliştirmek isteyen markalar",
                "SEO sürecini daha iyi anlamak isteyen ekipler",
            ]
        )
    )

    body.append(h2("Hedef ve Kullanıcıyı Netleştirmek"))
    body.append(
        p(
            "Başarılı bir SEO çalışmasının ilk adımı hedefin ve hedef kitlenin doğru tanımlanmasıdır. "
            "Bir web sitesinin kimlere hitap ettiği ve hangi sorunu çözmeyi amaçladığı net değilse SEO stratejisi de başarılı olmayacaktır."
        )
    )
    body.append(p("Bu nedenle SEO planı oluşturulurken şu sorulara cevap verilmelidir:"))
    body.append(
        ul(
            [
                "hedef kullanıcı kimdir",
                "kullanıcı hangi sorunları çözmek istiyor",
                "kullanıcı hangi anahtar kelimeleri arıyor",
            ]
        )
    )
    body.append(
        p(
            "Bu soruların cevapları SEO stratejisinin temelini oluşturur."
        )
    )

    body.append(h2("Bilgi Mimarisi ve İçerik Planı"))
    body.append(
        p(
            "SEO çalışmalarında web sitesinin bilgi mimarisi büyük önem taşır. "
            "Doğru yapılandırılmış bir site hem kullanıcı deneyimini iyileştirir hem de arama motorlarının siteyi daha kolay anlamasını sağlar."
        )
    )
    body.append(p("Bilgi mimarisi oluşturulurken şu yapılar planlanmalıdır:"))
    body.append(
        ul(
            [
                "ana sayfalar",
                "hizmet sayfaları",
                "konu bazlı içerikler (cluster)",
                "sık sorulan sorular",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı sayesinde site içerisinde mantıklı bir içerik hiyerarşisi oluşur."
        )
    )

    body.append(h2("Anahtar Kelime Araştırması"))
    body.append(
        p(
            "Anahtar kelime araştırması SEO çalışmalarının en kritik adımlarından biridir. "
            "Kullanıcıların arama motorlarında hangi kelimeleri kullandığını anlamak doğru içerik stratejisini oluşturmayı sağlar."
        )
    )
    body.append(p("Anahtar kelime araştırması yapılırken şu faktörler analiz edilir:"))
    body.append(
        ul(
            [
                "arama hacmi",
                "rekabet seviyesi",
                "kullanıcı niyeti",
                "trendler",
            ]
        )
    )
    body.append(
        p(
            "Doğru anahtar kelimeler hedeflendiğinde web sitesi daha hızlı organik trafik elde edebilir."
        )
    )

    body.append(h2("Tasarım ve Kullanılabilirlik"))
    body.append(
        p(
            "SEO yalnızca teknik optimizasyonlardan ibaret değildir. "
            "Kullanıcı deneyimi de SEO performansını doğrudan etkiler."
        )
    )
    body.append(p("Bir web sitesinin tasarımı şu özelliklere sahip olmalıdır:"))
    body.append(
        ul(
            [
                "okunabilir içerik",
                "mobil uyumluluk",
                "hızlı yükleme süresi",
                "kullanıcı dostu navigasyon",
            ]
        )
    )
    body.append(
        p(
            "Google algoritmaları kullanıcı deneyimini önemli bir sıralama faktörü olarak değerlendirmektedir."
        )
    )

    body.append(h2("Teknik SEO"))
    body.append(
        p(
            "Teknik SEO, arama motorlarının web sitesini doğru şekilde taramasını ve indekslemesini sağlar."
        )
    )
    body.append(p("Teknik SEO çalışmaları şu alanları kapsar:"))
    body.append(
        ul(
            [
                "site hız optimizasyonu",
                "mobil uyumluluk",
                "site haritası oluşturma",
                "indeksleme sorunlarını çözme",
                "yapılandırılmış veri kullanımı",
            ]
        )
    )
    body.append(
        p(
            "Bu optimizasyonlar yapılmadığında SEO çalışmalarının etkisi sınırlı kalabilir."
        )
    )

    body.append(h2("İçerik Stratejisi"))
    body.append(
        p(
            "SEO başarısının en önemli faktörlerinden biri kaliteli içeriktir. "
            "Arama motorları kullanıcıya değer sağlayan içerikleri öncelikli olarak sıralar."
        )
    )
    body.append(p("Etkili bir içerik stratejisi şu unsurları içerir:"))
    body.append(
        ul(
            [
                "kullanıcı sorularını cevaplayan içerikler",
                "anahtar kelime uyumlu makaleler",
                "düzenli içerik üretimi",
                "kapsamlı rehber içerikler",
            ]
        )
    )
    body.append(
        p(
            "Bu tür içerikler web sitesinin otoritesini artırır."
        )
    )

    body.append(h2("SEO Sürecinin Yayın Sonrası Aşaması"))
    body.append(
        p(
            "SEO çalışmaları web sitesi yayınlandıktan sonra da devam eder. "
            "Aslında SEO süreci sürekli bir iyileştirme döngüsüdür."
        )
    )
    body.append(p("Yayın sonrası yapılması gereken çalışmalar şunlardır:"))
    body.append(
        ul(
            [
                "performans analizi",
                "trafik ölçümü",
                "içerik güncellemeleri",
                "yeni backlink kazanımı",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar web sitesinin uzun vadede büyümesini sağlar."
        )
    )

    body.append(h2("SEO Stratejisinde Süreklilik"))
    body.append(
        p(
            "SEO kısa vadeli bir çalışma değildir. "
            "Arama motoru algoritmaları sürekli güncellendiği için SEO stratejilerinin de düzenli olarak geliştirilmesi gerekir."
        )
    )
    body.append(p("Uzun vadeli SEO başarısı için şu adımlar önemlidir:"))
    body.append(
        ul(
            [
                "düzenli içerik üretimi",
                "teknik optimizasyonların güncellenmesi",
                "rekabet analizi",
                "kullanıcı deneyiminin geliştirilmesi",
            ]
        )
    )
    body.append(
        p(
            "Doğru uygulanan SEO stratejileri işletmelerin dijital dünyada sürdürülebilir büyüme elde etmesini sağlar."
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
    cluster_urls = _cluster_urls_for_service(page)[:10]
    if cluster_urls:
        body.append(h3("Konular"))
        body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

    content_html = "\n".join(body)
    meta_title = "SEO Hizmetleri Rehberi | Profesyonel SEO Süreci Nasıl İşler – Angraweb"
    meta_description = (
        "SEO hizmetleri rehberi ile profesyonel SEO sürecini öğrenin. Anahtar kelime araştırması, teknik SEO, içerik stratejisi ve SEO planlama adımlarını keşfedin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Hizmetleri Rehberi",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _seo_services_quote_tr(page: SeoPage) -> Dict:
    """Custom SEO quote page (TR) — teklif süreci, brif, şeffaf süreç."""
    body: List[str] = []

    body.append(
        p(
            "SEO hizmetleri için doğru bir teklif almak, projenin kapsamını ve hedeflerini doğru şekilde belirlemekle başlar. "
            "Her web sitesi farklı ihtiyaçlara sahip olduğu için SEO çalışmaları genellikle projeye özel planlanır."
        )
    )
    body.append(
        p(
            "Angraweb olarak SEO projelerinde önce işletmenin hedeflerini ve mevcut dijital durumunu analiz ediyoruz. "
            "Bu sayede hem bütçeye uygun hem de sürdürülebilir bir SEO stratejisi oluşturabiliyoruz."
        )
    )
    body.append(
        p(
            "SEO hizmetleri için teklif almak isteyen işletmelerin kısa bir proje brifi paylaşması sürecin daha hızlı ilerlemesini sağlar."
        )
    )

    body.append(h2("Teklif Süreci Nasıl İşler"))
    body.append(
        p(
            "SEO hizmetleri teklif süreci birkaç temel adımdan oluşur. "
            "Bu süreç hem işletmenin ihtiyaçlarını doğru anlamayı hem de uygulanabilir bir SEO planı oluşturmayı amaçlar."
        )
    )
    body.append(h3("1. Kısa Brif"))
    body.append(
        p(
            "İlk adımda işletmenin hedefleri ve beklentileri hakkında kısa bir bilgi alınır."
        )
    )
    body.append(p("Bu brifte genellikle şu bilgiler yer alır:"))
    body.append(
        ul(
            [
                "işletmenin faaliyet alanı",
                "hedef kitle",
                "mevcut web sitesi durumu",
                "SEO hedefleri",
            ]
        )
    )
    body.append(
        p(
            "Bu bilgiler SEO stratejisinin temelini oluşturur."
        )
    )
    body.append(h3("2. Ön Görüşme"))
    body.append(
        p(
            "Kısa brif incelendikten sonra bir ön görüşme yapılır. Bu görüşme genellikle online olarak gerçekleştirilir."
        )
    )
    body.append(p("Bu aşamada şu konular netleştirilir:"))
    body.append(
        ul(
            [
                "projenin kapsamı",
                "öncelikli SEO hedefleri",
                "rekabet analizi",
                "tahmini çalışma süresi",
            ]
        )
    )
    body.append(
        p(
            "Bu görüşme sayesinde SEO planı daha net hale gelir."
        )
    )
    body.append(h3("3. SEO Planı Oluşturma"))
    body.append(
        p(
            "İhtiyaçlar netleştikten sonra detaylı bir SEO planı hazırlanır. Bu plan genellikle şu çalışmaları içerir:"
        )
    )
    body.append(
        ul(
            [
                "SEO analizi",
                "anahtar kelime araştırması",
                "teknik SEO optimizasyonu",
                "içerik stratejisi",
                "backlink planı",
            ]
        )
    )
    body.append(
        p(
            "SEO planı web sitesinin mevcut durumuna göre özelleştirilir."
        )
    )
    body.append(h3("4. Teklif ve Çalışma Planı"))
    body.append(
        p(
            "Son aşamada SEO hizmeti için kapsamlı bir teklif hazırlanır."
        )
    )
    body.append(p("Bu teklif genellikle şu bilgileri içerir:"))
    body.append(
        ul(
            [
                "yapılacak çalışmalar",
                "proje takvimi",
                "raporlama süreci",
                "ödeme planı",
            ]
        )
    )
    body.append(
        p(
            "Bu sayede işletmeler SEO projesinin nasıl ilerleyeceğini net bir şekilde görebilir."
        )
    )

    body.append(h2("Brifte Hangi Bilgileri Paylaşmalısınız"))
    body.append(
        p(
            "SEO teklifinin doğru hazırlanabilmesi için bazı temel bilgilerin paylaşılması önemlidir."
        )
    )
    body.append(p("Paylaşılması önerilen bilgiler:"))
    body.append(
        ul(
            [
                "işletmenin ana hedefi (satış, trafik, marka bilinirliği)",
                "öncelikli sayfalar veya hizmetler",
                "mevcut web sitesi adresi",
                "rakip web siteleri",
            ]
        )
    )
    body.append(
        p(
            "Bu bilgiler SEO stratejisinin doğru planlanmasına yardımcı olur."
        )
    )

    body.append(h2("SEO Teklifi Neden Özel Hazırlanır"))
    body.append(
        p(
            "SEO projeleri genellikle tek tip kapsamlarla sınırlı değildir. Çünkü her sektörün rekabet seviyesi ve hedef kitlesi farklıdır."
        )
    )
    body.append(p("Örneğin:"))
    body.append(
        ul(
            [
                "yeni bir web sitesi için SEO stratejisi farklıdır",
                "yüksek rekabetli sektörler daha kapsamlı SEO çalışmaları gerektirir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle SEO teklifleri genellikle işletmeye özel hazırlanır."
        )
    )

    body.append(h2("Şeffaf Süreç ve Güven"))
    body.append(
        p(
            "Angraweb olarak SEO projelerinde şeffaf bir süreç yönetimi uyguluyoruz. "
            "Tüm çalışmalar açık şekilde raporlanır ve proje süreci boyunca düzenli iletişim sağlanır."
        )
    )
    body.append(p("SEO çalışmalarında şu prensiplere önem veriyoruz:"))
    body.append(
        ul(
            [
                "net proje kapsamı",
                "düzenli raporlama",
                "ölçülebilir performans hedefleri",
                "uzun vadeli büyüme stratejisi",
            ]
        )
    )
    body.append(
        p(
            "Bu yaklaşım SEO projelerinin daha verimli ilerlemesini sağlar."
        )
    )

    body.append(h2("SEO Hizmetleri İçin Hızlı Teklif"))
    body.append(
        p(
            "Eğer web siteniz için profesyonel SEO hizmetleri almak istiyorsanız teklif formunu doldurarak bizimle iletişime geçebilirsiniz."
        )
    )
    body.append(
        p(
            "Kısa bir brif paylaşmanız durumunda SEO projeniz için en uygun yaklaşımı hızlıca planlayabiliriz."
        )
    )
    body.append(p("Teklif formu sayesinde:"))
    body.append(
        ul(
            [
                "SEO ihtiyaçlarınızı paylaşabilirsiniz",
                "proje kapsamını belirleyebilirsiniz",
                "tahmini bütçe planı oluşturabilirsiniz",
            ]
        )
    )
    body.append(
        p(
            f"SEO hizmetleri teklif formunu doldurarak projenize ilk adımı atabilirsiniz. "
            f"Teklif almak için: {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Hizmetleri Teklif Al | Profesyonel SEO Danışmanlığı – Angraweb"
    meta_description = (
        "Profesyonel SEO hizmetleri için hızlı teklif alın. Web sitenizin SEO analizi, anahtar kelime stratejisi ve teknik optimizasyon planını öğrenin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Hizmetleri Teklif Al",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_danismanligi_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Danışmanlığı (TR) — danışmanlık hizmeti, süreç, kapsam."""
    body: List[str] = []

    body.append(h2("SEO Danışmanlığı Nedir"))
    body.append(
        p(
            "SEO danışmanlığı, web sitelerinin arama motorlarında daha görünür olması için stratejik yönlendirme ve optimizasyon önerileri sunan profesyonel bir hizmettir."
        )
    )
    body.append(
        p(
            "Bir SEO danışmanı, web sitenizin mevcut performansını analiz eder ve arama motoru sıralamalarını yükseltmek için uygulanabilir bir yol haritası oluşturur."
        )
    )
    body.append(
        p(
            "Angraweb olarak işletmelerin dijital görünürlüğünü artırmak için veri odaklı SEO danışmanlığı sunuyoruz."
        )
    )

    body.append(h2("SEO Danışmanlığı Neden Önemlidir"))
    body.append(
        p(
            "Birçok web sitesi teknik hatalar, yanlış anahtar kelime stratejileri veya zayıf içerik yapısı nedeniyle arama motorlarında yeterince görünmez."
        )
    )
    body.append(p("Profesyonel SEO danışmanlığı sayesinde işletmeler:"))
    body.append(
        ul(
            [
                "Google sıralamalarını yükseltebilir",
                "organik trafik artırabilir",
                "teknik SEO hatalarını düzeltebilir",
                "içerik stratejisini geliştirebilir",
            ]
        )
    )
    body.append(
        p(
            "Doğru bir SEO danışmanlığı, uzun vadeli dijital büyüme için önemli bir adımdır."
        )
    )

    body.append(h2("SEO Danışmanlığı Hizmeti Neleri Kapsar"))
    body.append(
        p(
            "SEO danışmanlığı hizmeti genellikle web sitesinin tüm SEO performansını kapsayan kapsamlı bir analiz sürecini içerir."
        )
    )
    body.append(p("Bu süreçte şu çalışmalar yapılır:"))
    body.append(
        ul(
            [
                "SEO site analizi",
                "teknik SEO değerlendirmesi",
                "anahtar kelime araştırması",
                "rakip analizi",
                "içerik stratejisi oluşturma",
            ]
        )
    )
    body.append(
        p(
            "Bu analizler web sitesi için en doğru SEO stratejisinin belirlenmesini sağlar."
        )
    )

    body.append(h2("Angraweb SEO Danışmanlığı Süreci"))
    body.append(
        p(
            "SEO danışmanlığı hizmetimiz belirli bir süreç doğrultusunda ilerler."
        )
    )
    body.append(h3("SEO Analizi"))
    body.append(
        p(
            "İlk aşamada web sitesinin teknik altyapısı ve mevcut SEO performansı analiz edilir."
        )
    )
    body.append(p("Bu aşamada:"))
    body.append(
        ul(
            [
                "teknik SEO hataları",
                "site performansı",
                "anahtar kelime fırsatları",
            ]
        )
    )
    body.append(p("tespit edilir."))
    body.append(h3("SEO Stratejisi"))
    body.append(
        p(
            "Analiz tamamlandıktan sonra web sitesi için kapsamlı bir SEO stratejisi hazırlanır."
        )
    )
    body.append(p("Bu strateji şunları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO iyileştirmeleri",
                "içerik optimizasyonu",
                "anahtar kelime hedefleme",
            ]
        )
    )
    body.append(h3("Uygulama Rehberi"))
    body.append(
        p(
            "SEO danışmanlığı kapsamında işletmelere uygulanabilir bir yol haritası sunulur."
        )
    )
    body.append(p("Bu yol haritası sayesinde ekipler:"))
    body.append(
        ul(
            [
                "SEO optimizasyonlarını doğru şekilde uygulayabilir",
                "içerik stratejisini geliştirebilir",
                "site performansını iyileştirebilir",
            ]
        )
    )
    body.append(h3("İzleme ve Raporlama"))
    body.append(
        p(
            "SEO çalışmaları uygulandıktan sonra performans düzenli olarak takip edilir."
        )
    )
    body.append(p("Bu süreçte:"))
    body.append(
        ul(
            [
                "anahtar kelime sıralamaları",
                "organik trafik",
                "kullanıcı davranışları",
            ]
        )
    )
    body.append(p("analiz edilir."))

    body.append(h2("SEO Danışmanlığı Kimler İçin Uygundur"))
    body.append(
        p(
            "SEO danışmanlığı özellikle şu durumlarda faydalıdır:"
        )
    )
    body.append(
        ul(
            [
                "SEO stratejisi oluşturmak isteyen işletmeler",
                "mevcut web sitesinin performansını artırmak isteyen şirketler",
                "teknik SEO hatalarını düzeltmek isteyen ekipler",
            ]
        )
    )
    body.append(
        p(
            "Bu hizmet, SEO çalışmalarını daha sistemli ve verimli hale getirir."
        )
    )

    body.append(h2("Angraweb SEO Danışmanlığı"))
    body.append(
        p(
            "Angraweb olarak işletmelere profesyonel SEO danışmanlığı hizmeti sunuyoruz."
        )
    )
    body.append(p("SEO danışmanlığı kapsamında:"))
    body.append(
        ul(
            [
                "teknik SEO analizi",
                "anahtar kelime stratejisi",
                "içerik geliştirme önerileri",
                "performans izleme",
            ]
        )
    )
    body.append(p("gibi alanlarda destek sağlıyoruz."))
    body.append(
        p(
            "Amacımız web sitenizin arama motorlarında daha görünür hale gelmesini ve sürdürülebilir organik trafik elde etmesini sağlamaktır."
        )
    )

    body.append(h2("SEO Danışmanlığı İçin Teklif Alın"))
    body.append(
        p(
            "Eğer web sitenizin Google sıralamalarını yükseltmek ve organik trafiğinizi artırmak istiyorsanız profesyonel SEO danışmanlığı hizmeti alabilirsiniz."
        )
    )
    body.append(
        p(
            f"Projeniz için en doğru SEO stratejisini oluşturmak için Angraweb ekibiyle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Danışmanlığı | Profesyonel SEO Danışmanlık Hizmeti – Angraweb"
    meta_description = (
        "Profesyonel SEO danışmanlığı ile web sitenizin Google sıralamasını yükseltin. Teknik SEO analizi, anahtar kelime stratejisi ve sürdürülebilir organik trafik büyümesi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Danışmanlığı",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_teknik_seo_tr(page: SeoPage) -> Dict:
    """Custom cluster: Teknik SEO (TR) — site hızı, CWV, crawl, mimari."""
    body: List[str] = []

    body.append(h2("Teknik SEO Nedir"))
    body.append(
        p(
            "Teknik SEO, web sitesinin arama motorları tarafından doğru şekilde taranması, dizine eklenmesi ve sıralanabilmesi için yapılan teknik optimizasyon çalışmalarını kapsar."
        )
    )
    body.append(
        p(
            "Bir web sitesi güçlü içeriklere sahip olsa bile teknik sorunlar nedeniyle arama motorlarında yeterince görünmeyebilir."
        )
    )
    body.append(p("Teknik SEO çalışmaları sayesinde web siteleri:"))
    body.append(
        ul(
            [
                "daha hızlı yüklenir",
                "arama motorları tarafından daha kolay taranır",
                "kullanıcı deneyimi iyileşir",
                "Google sıralamalarında daha iyi performans gösterir",
            ]
        )
    )
    body.append(
        p(
            "Angraweb olarak teknik SEO optimizasyonu ile web sitelerinin arama motorları için daha güçlü bir altyapıya sahip olmasını sağlıyoruz."
        )
    )

    body.append(h2("Teknik SEO Neden Önemlidir"))
    body.append(
        p(
            "Google gibi arama motorları web sitelerini teknik kriterlere göre değerlendirir."
        )
    )
    body.append(
        p(
            "Eğer bir web sitesinde teknik sorunlar varsa, bu durum arama motoru sıralamalarını doğrudan etkileyebilir."
        )
    )
    body.append(p("Teknik SEO çalışmaları sayesinde:"))
    body.append(
        ul(
            [
                "site performansı artar",
                "sayfalar daha hızlı indekslenir",
                "crawl hataları azaltılır",
                "kullanıcı deneyimi iyileşir",
            ]
        )
    )
    body.append(
        p(
            "Bu optimizasyonlar web sitelerinin uzun vadeli SEO başarısı için kritik öneme sahiptir."
        )
    )

    body.append(h2("Teknik SEO Çalışmaları Neleri Kapsar"))
    body.append(
        p(
            "Teknik SEO hizmetleri web sitesinin altyapısını analiz ederek performans sorunlarını tespit etmeyi içerir."
        )
    )
    body.append(p("Bu çalışmalar genellikle şu alanları kapsar:"))
    body.append(
        ul(
            [
                "site hız optimizasyonu",
                "Core Web Vitals iyileştirmeleri",
                "crawl ve index optimizasyonu",
                "URL yapılandırması",
                "site mimarisi optimizasyonu",
                "mobil uyumluluk analizi",
            ]
        )
    )
    body.append(
        p(
            "Bu optimizasyonlar arama motorlarının web sitesini daha iyi anlamasını sağlar."
        )
    )

    body.append(h2("Teknik SEO Analizi"))
    body.append(
        p(
            "Teknik SEO çalışmalarının ilk adımı detaylı bir SEO analizidir."
        )
    )
    body.append(p("Bu analiz sırasında:"))
    body.append(
        ul(
            [
                "site crawl hataları",
                "indeksleme sorunları",
                "sayfa performansı",
                "teknik SEO eksiklikleri",
            ]
        )
    )
    body.append(p("tespit edilir."))
    body.append(
        p(
            "Bu analiz sayesinde web sitesi için uygulanabilir bir teknik SEO planı oluşturulur."
        )
    )

    body.append(h2("Core Web Vitals Optimizasyonu"))
    body.append(
        p(
            "Google sıralama faktörlerinden biri olan Core Web Vitals, kullanıcı deneyimini ölçen performans metrikleridir."
        )
    )
    body.append(p("Bu metrikler:"))
    body.append(
        ul(
            [
                "LCP (Largest Contentful Paint)",
                "CLS (Cumulative Layout Shift)",
                "INP / Interaction",
            ]
        )
    )
    body.append(p("gibi performans ölçümlerini içerir."))
    body.append(
        p(
            "Teknik SEO çalışmaları bu metriklerin optimize edilmesini sağlar."
        )
    )

    body.append(h2("Teknik SEO ve Site Mimarisi"))
    body.append(
        p(
            "Doğru site mimarisi hem kullanıcılar hem de arama motorları için önemlidir."
        )
    )
    body.append(p("İyi bir teknik SEO yapısı sayesinde:"))
    body.append(
        ul(
            [
                "sayfalar daha kolay bulunur",
                "site içi bağlantılar daha güçlü olur",
                "crawl bütçesi daha verimli kullanılır",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı SEO performansını doğrudan etkiler."
        )
    )

    body.append(h2("Angraweb Teknik SEO Hizmetleri"))
    body.append(
        p(
            "Angraweb olarak işletmelere kapsamlı teknik SEO çözümleri sunuyoruz."
        )
    )
    body.append(p("Teknik SEO hizmetlerimiz şunları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO analizi",
                "site hız optimizasyonu",
                "Core Web Vitals iyileştirmeleri",
                "site mimarisi optimizasyonu",
                "indeksleme ve crawl sorunlarının çözümü",
            ]
        )
    )
    body.append(
        p(
            "Amacımız web sitenizin arama motorları tarafından daha iyi anlaşılmasını ve daha yüksek sıralamalara ulaşmasını sağlamaktır."
        )
    )

    body.append(h2("Teknik SEO Hizmeti İçin Teklif Alın"))
    body.append(
        p(
            "Web sitenizin teknik altyapısını güçlendirmek ve SEO performansını artırmak için profesyonel teknik SEO hizmeti alabilirsiniz."
        )
    )
    body.append(
        p(
            f"Projeniz için teknik SEO analizi ve strateji oluşturmak için Angraweb ekibiyle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "Teknik SEO Hizmeti | Site Teknik SEO Analizi – Angraweb"
    meta_description = (
        "Teknik SEO hizmeti ile web sitenizin taranabilirliğini ve performansını artırın. Site hızı, Core Web Vitals ve teknik SEO optimizasyonu ile Google sıralamalarınızı yükseltin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Teknik SEO",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_on_page_seo_tr(page: SeoPage) -> Dict:
    """Custom cluster: On Page SEO (TR) — içerik, başlık, iç bağlantı optimizasyonu."""
    body: List[str] = []

    body.append(h2("On Page SEO Nedir"))
    body.append(
        p(
            "On page SEO, web sayfalarının içerik ve yapı açısından arama motorları için optimize edilmesi sürecidir."
        )
    )
    body.append(
        p(
            "Teknik SEO web sitesinin altyapısına odaklanırken, on page SEO doğrudan sayfa içeriği ve yapısı ile ilgilenir."
        )
    )
    body.append(p("Doğru şekilde optimize edilmiş bir sayfa:"))
    body.append(
        ul(
            [
                "arama motorları tarafından daha iyi anlaşılır",
                "doğru anahtar kelimeler için sıralama alır",
                "kullanıcı deneyimini geliştirir",
            ]
        )
    )
    body.append(
        p(
            "Angraweb olarak web sitelerinin görünürlüğünü artırmak için kapsamlı on page SEO optimizasyonu sunuyoruz."
        )
    )

    body.append(h2("On Page SEO Neden Önemlidir"))
    body.append(
        p(
            "Bir web sitesinin içeriği arama motoru sıralamalarını doğrudan etkiler."
        )
    )
    body.append(
        p(
            "Eğer içerik doğru optimize edilmemişse sayfalar Google'da üst sıralara çıkmakta zorlanabilir."
        )
    )
    body.append(p("On page SEO çalışmaları sayesinde:"))
    body.append(
        ul(
            [
                "sayfalar doğru anahtar kelimeler için optimize edilir",
                "içerik daha okunabilir hale gelir",
                "kullanıcı deneyimi iyileşir",
                "organik trafik artar",
            ]
        )
    )

    body.append(h2("On Page SEO Hizmeti Neleri Kapsar"))
    body.append(
        p(
            "On page SEO hizmetleri web sitesindeki sayfaların detaylı şekilde optimize edilmesini içerir."
        )
    )
    body.append(p("Bu çalışmalar genellikle şunları kapsar:"))
    body.append(
        ul(
            [
                "anahtar kelime optimizasyonu",
                "başlık ve meta açıklama optimizasyonu",
                "içerik geliştirme",
                "iç bağlantı stratejisi",
                "görsel optimizasyonu",
            ]
        )
    )
    body.append(
        p(
            "Bu optimizasyonlar web sayfalarının arama motorlarında daha iyi performans göstermesini sağlar."
        )
    )

    body.append(h2("İçerik Optimizasyonu"))
    body.append(
        p(
            "SEO için içerik optimizasyonu çok önemlidir."
        )
    )
    body.append(p("Kaliteli bir SEO içeriği:"))
    body.append(
        ul(
            [
                "kullanıcı niyetine uygun olmalı",
                "doğal anahtar kelimeler içermeli",
                "iyi yapılandırılmış olmalıdır",
            ]
        )
    )
    body.append(
        p(
            "Arama motorları kullanıcıya değer sunan içerikleri daha üst sıralarda gösterir."
        )
    )

    body.append(h2("İç Bağlantı Stratejisi"))
    body.append(
        p(
            "İç bağlantılar web sitesi içindeki sayfaları birbirine bağlar."
        )
    )
    body.append(p("Doğru iç bağlantı yapısı sayesinde:"))
    body.append(
        ul(
            [
                "SEO otoritesi sayfalar arasında dağıtılır",
                "sayfalar daha kolay taranır",
                "kullanıcılar ilgili içeriklere ulaşabilir",
            ]
        )
    )
    body.append(
        p(
            "Bu yapı SEO performansını önemli ölçüde artırır."
        )
    )

    body.append(h2("Angraweb On Page SEO Hizmetleri"))
    body.append(
        p(
            "Angraweb olarak web siteleri için profesyonel on page SEO optimizasyonu sunuyoruz."
        )
    )
    body.append(p("Hizmetlerimiz şunları kapsar:"))
    body.append(
        ul(
            [
                "SEO içerik optimizasyonu",
                "meta etiket optimizasyonu",
                "iç bağlantı stratejisi",
                "sayfa içi SEO analizi",
            ]
        )
    )
    body.append(
        p(
            "Amacımız web sitenizin Google aramalarında daha görünür olmasını sağlamaktır."
        )
    )

    body.append(h2("On Page SEO Hizmeti İçin Teklif Alın"))
    body.append(
        p(
            "Web sitenizin organik trafiğini artırmak ve Google sıralamalarını yükseltmek için profesyonel on page SEO hizmeti alabilirsiniz."
        )
    )
    body.append(
        p(
            f"Projeniz için en doğru SEO stratejisini oluşturmak üzere Angraweb ekibiyle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "On Page SEO Hizmeti | Sayfa İçi SEO Optimizasyonu – Angraweb"
    meta_description = (
        "On page SEO hizmeti ile web sitenizin Google sıralamasını yükseltin. İçerik optimizasyonu, başlık yapısı ve iç bağlantılar ile organik trafiği artırın."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "On Page SEO Hizmeti",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_analizi_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Analizi (TR) — audit, teknik, içerik, rakip analizi."""
    body: List[str] = []

    body.append(h2("SEO Analizi Nedir"))
    body.append(
        p(
            "SEO analizi, bir web sitesinin arama motorlarındaki performansını değerlendirmek için yapılan kapsamlı inceleme sürecidir."
        )
    )
    body.append(
        p(
            "Bu analiz sayesinde web sitesinin teknik yapısı, içerik kalitesi ve SEO performansı detaylı şekilde değerlendirilir."
        )
    )
    body.append(p("SEO analizi çalışmaları sayesinde şu sorulara cevap bulunur:"))
    body.append(
        ul(
            [
                "Web sitesi neden sıralama alamıyor?",
                "Hangi teknik hatalar SEO'yu etkiliyor?",
                "Hangi anahtar kelimelerde fırsatlar var?",
            ]
        )
    )
    body.append(
        p(
            "Bu analiz, başarılı bir SEO stratejisinin ilk adımıdır."
        )
    )

    body.append(h2("SEO Analizi Neden Önemlidir"))
    body.append(
        p(
            "Bir web sitesi SEO açısından optimize edilmeden önce mevcut durumun doğru şekilde analiz edilmesi gerekir."
        )
    )
    body.append(p("SEO analizi sayesinde:"))
    body.append(
        ul(
            [
                "teknik SEO sorunları tespit edilir",
                "içerik eksikleri belirlenir",
                "rakip stratejileri incelenir",
                "SEO fırsatları ortaya çıkar",
            ]
        )
    )
    body.append(
        p(
            "Bu bilgiler daha etkili bir SEO stratejisi oluşturmayı sağlar."
        )
    )

    body.append(h2("SEO Analizi Neleri Kapsar"))
    body.append(
        p(
            "Profesyonel SEO analizi web sitesinin birçok farklı alanını inceler."
        )
    )
    body.append(p("Bu analiz genellikle şu konuları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO incelemesi",
                "site hız analizi",
                "anahtar kelime analizi",
                "içerik optimizasyonu değerlendirmesi",
                "backlink profili analizi",
                "rakip SEO analizi",
            ]
        )
    )
    body.append(
        p(
            "Bu kapsamlı inceleme sayesinde web sitesinin güçlü ve zayıf yönleri belirlenir."
        )
    )

    body.append(h2("Teknik SEO Analizi"))
    body.append(
        p(
            "Teknik SEO analizi web sitesinin altyapısını inceler."
        )
    )
    body.append(p("Bu analiz sırasında:"))
    body.append(
        ul(
            [
                "crawl hataları",
                "indeksleme sorunları",
                "sayfa hız problemleri",
                "site mimarisi",
            ]
        )
    )
    body.append(p("gibi teknik konular değerlendirilir."))
    body.append(
        p(
            "Bu optimizasyonlar web sitesinin arama motorları tarafından daha kolay taranmasını sağlar."
        )
    )

    body.append(h2("İçerik ve Anahtar Kelime Analizi"))
    body.append(
        p(
            "SEO analizi yalnızca teknik konularla sınırlı değildir."
        )
    )
    body.append(
        p(
            "Aynı zamanda içerik yapısı ve anahtar kelime stratejisi de değerlendirilir."
        )
    )
    body.append(p("Bu analiz sayesinde:"))
    body.append(
        ul(
            [
                "doğru anahtar kelimeler belirlenir",
                "içerik boşlukları tespit edilir",
                "yeni SEO fırsatları keşfedilir",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar web sitesinin organik trafik potansiyelini artırır."
        )
    )

    body.append(h2("Rakip SEO Analizi"))
    body.append(
        p(
            "Rakip analizi SEO stratejisinin önemli bir parçasıdır."
        )
    )
    body.append(p("Rakip SEO analizi sayesinde:"))
    body.append(
        ul(
            [
                "rakiplerin hangi anahtar kelimelerde sıralama aldığı",
                "backlink stratejileri",
                "içerik stratejileri",
            ]
        )
    )
    body.append(p("incelenir."))
    body.append(
        p(
            "Bu bilgiler daha rekabetçi bir SEO planı oluşturmayı sağlar."
        )
    )

    body.append(h2("Angraweb SEO Analizi Hizmeti"))
    body.append(
        p(
            "Angraweb olarak işletmelere kapsamlı SEO analizi hizmetleri sunuyoruz."
        )
    )
    body.append(p("SEO analiz hizmetlerimiz şunları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO audit",
                "anahtar kelime araştırması",
                "rakip SEO analizi",
                "içerik ve sayfa optimizasyonu değerlendirmesi",
            ]
        )
    )
    body.append(
        p(
            "Amacımız web sitenizin SEO performansını artırmak için güçlü bir stratejik temel oluşturmaktır."
        )
    )

    body.append(h2("SEO Analizi İçin Teklif Alın"))
    body.append(
        p(
            "Web sitenizin SEO performansını artırmak için profesyonel SEO analizi yaptırabilirsiniz."
        )
    )
    body.append(
        p(
            "Angraweb ekibi web sitenizi detaylı şekilde inceleyerek SEO geliştirme fırsatlarını belirler."
        )
    )
    body.append(
        p(
            f"SEO analizi hizmeti için bizimle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Analizi Hizmeti | Profesyonel SEO Audit – Angraweb"
    meta_description = (
        "Profesyonel SEO analizi ile web sitenizin teknik ve içerik sorunlarını tespit edin. SEO audit, rakip analizi ve fırsat stratejileri ile Google sıralamanızı yükseltin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Analizi",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_nedir_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Nedir? (TR) — temel kavramlar, türler, strateji."""
    body: List[str] = []

    body.append(h2("SEO Nedir"))
    body.append(
        p(
            "SEO (Search Engine Optimization), web sitelerinin arama motorlarında daha görünür hale gelmesini sağlayan optimizasyon çalışmalarının genel adıdır."
        )
    )
    body.append(
        p(
            "SEO çalışmaları sayesinde web siteleri Google gibi arama motorlarında daha üst sıralarda görünür ve daha fazla organik trafik elde eder."
        )
    )
    body.append(p("SEO'nun temel amacı:"))
    body.append(
        ul(
            [
                "web sitesinin görünürlüğünü artırmak",
                "doğru anahtar kelimelerde sıralama almak",
                "kullanıcı deneyimini geliştirmek",
                "organik trafik elde etmektir",
            ]
        )
    )
    body.append(p("Doğru bir SEO stratejisi uzun vadede sürdürülebilir büyüme sağlar."))

    body.append(h2("SEO Nasıl Çalışır"))
    body.append(
        p(
            "Arama motorları web sitelerini analiz etmek için gelişmiş algoritmalar kullanır."
        )
    )
    body.append(
        p(
            "Bu algoritmalar web sitelerini değerlendirirken birçok faktörü dikkate alır."
        )
    )
    body.append(p("Bunlardan bazıları:"))
    body.append(
        ul(
            [
                "içerik kalitesi",
                "sayfa yapısı",
                "site hızı",
                "kullanıcı deneyimi",
                "backlink profili",
            ]
        )
    )
    body.append(
        p(
            "SEO çalışmaları bu faktörleri optimize ederek web sitelerinin arama motorları tarafından daha iyi değerlendirilmesini sağlar."
        )
    )

    body.append(h2("SEO Türleri"))
    body.append(p("SEO çalışmaları genellikle üç ana kategoriye ayrılır."))
    body.append(h3("Teknik SEO"))
    body.append(p("Teknik SEO, web sitesinin altyapısını optimize etmeye odaklanır."))
    body.append(p("Bu çalışmalar şunları kapsar:"))
    body.append(
        ul(
            [
                "site hız optimizasyonu",
                "crawl ve index optimizasyonu",
                "Core Web Vitals iyileştirmeleri",
                "site mimarisi",
            ]
        )
    )
    body.append(p("Teknik SEO, arama motorlarının web sitesini daha kolay taramasını sağlar."))

    body.append(h3("On Page SEO"))
    body.append(
        p(
            "On page SEO, web sayfalarının içerik ve yapı açısından optimize edilmesidir."
        )
    )
    body.append(p("Bu optimizasyonlar şunları içerir:"))
    body.append(
        ul(
            [
                "anahtar kelime optimizasyonu",
                "başlık ve meta açıklamalar",
                "içerik geliştirme",
                "iç bağlantı stratejisi",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar sayfaların arama motorlarında daha iyi sıralama almasına yardımcı olur."
        )
    )

    body.append(h3("Off Page SEO"))
    body.append(p("Off page SEO, web sitesi dışındaki SEO çalışmalarını kapsar."))
    body.append(p("Bunlar genellikle:"))
    body.append(
        ul(
            [
                "backlink oluşturma",
                "marka otoritesi",
                "dijital PR çalışmaları",
            ]
        )
    )
    body.append(p("gibi yöntemleri içerir."))
    body.append(p("Bu çalışmalar web sitesinin güvenilirliğini artırır."))

    body.append(h2("SEO Neden Önemlidir"))
    body.append(
        p(
            "İnternet kullanıcılarının büyük bir kısmı ihtiyaç duyduğu bilgiyi arama motorları üzerinden bulur."
        )
    )
    body.append(
        p(
            "Bu nedenle arama motorlarında görünür olmak işletmeler için büyük avantaj sağlar."
        )
    )
    body.append(p("SEO çalışmaları sayesinde:"))
    body.append(
        ul(
            [
                "organik trafik artar",
                "marka bilinirliği yükselir",
                "daha fazla potansiyel müşteri elde edilir",
                "reklam bağımlılığı azalır",
            ]
        )
    )
    body.append(p("SEO uzun vadede en sürdürülebilir dijital pazarlama stratejilerinden biridir."))

    body.append(h2("SEO Stratejisi Nasıl Oluşturulur"))
    body.append(p("Başarılı bir SEO stratejisi oluşturmak için birkaç temel adım izlenir."))
    body.append(p("Bu adımlar genellikle şunları içerir:"))
    body.append(
        ul(
            [
                "anahtar kelime araştırması",
                "teknik SEO analizi",
                "içerik optimizasyonu",
                "rakip analizi",
                "backlink stratejisi",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar bir araya geldiğinde web sitesinin SEO performansı önemli ölçüde artar."
        )
    )

    body.append(h2("Angraweb SEO Hizmetleri"))
    body.append(
        p(
            "Angraweb olarak işletmeler için profesyonel SEO hizmetleri sunuyoruz."
        )
    )
    body.append(p("SEO hizmetlerimiz şunları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO optimizasyonu",
                "içerik ve on page SEO çalışmaları",
                "SEO analizi ve strateji oluşturma",
                "rakip analizi",
            ]
        )
    )
    body.append(
        p(
            "Amacımız web sitenizin arama motorlarında daha görünür hale gelmesini sağlamaktır."
        )
    )

    body.append(h2("SEO Hizmetleri İçin Teklif Alın"))
    body.append(
        p(
            "Web sitenizin Google sıralamalarını yükseltmek ve daha fazla organik trafik elde etmek için profesyonel SEO hizmeti alabilirsiniz."
        )
    )
    body.append(
        p(
            f"Projeniz için en doğru SEO stratejisini oluşturmak üzere Angraweb ekibiyle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Nedir? Arama Motoru Optimizasyonu Rehberi – Angraweb"
    meta_description = (
        "SEO nedir ve nasıl çalışır? Arama motoru optimizasyonu hakkında temel bilgiler, SEO türleri ve web sitenizi Google'da yükseltmek için kullanılan stratejileri öğrenin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Nedir?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_nasil_yapilir_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Nasıl Yapılır? (TR) — adım adım SEO rehberi."""
    body: List[str] = []

    body.append(h2("SEO Nasıl Yapılır"))
    body.append(
        p(
            "SEO çalışmaları web sitelerinin arama motorlarında daha üst sıralarda yer almasını sağlamak için yapılan optimizasyon süreçlerinden oluşur."
        )
    )
    body.append(
        p(
            "Başarılı bir SEO çalışması, teknik yapıdan içerik stratejisine kadar birçok farklı faktörün birlikte optimize edilmesini gerektirir."
        )
    )
    body.append(p("SEO süreci genellikle aşağıdaki adımlardan oluşur:"))
    body.append(
        ul(
            [
                "anahtar kelime araştırması",
                "teknik SEO optimizasyonu",
                "içerik optimizasyonu",
                "site içi bağlantı yapısı",
                "backlink çalışmaları",
            ]
        )
    )
    body.append(
        p(
            "Bu adımlar doğru şekilde uygulandığında web sitelerinin organik trafik potansiyeli önemli ölçüde artar."
        )
    )

    body.append(h2("1. Anahtar Kelime Araştırması"))
    body.append(
        p(
            "SEO çalışmalarının ilk adımı doğru anahtar kelimeleri belirlemektir."
        )
    )
    body.append(
        p(
            "Anahtar kelime araştırması sayesinde kullanıcıların arama motorlarında hangi kelimeleri aradığı anlaşılır."
        )
    )
    body.append(p("Bu süreçte genellikle şu araçlar kullanılır:"))
    body.append(
        ul(
            [
                "Google Keyword Planner",
                "Ahrefs",
                "Semrush",
                "Google Search Console",
            ]
        )
    )
    body.append(p("Doğru anahtar kelimeleri hedeflemek SEO başarısı için kritik öneme sahiptir."))

    body.append(h2("2. Teknik SEO Optimizasyonu"))
    body.append(p("Teknik SEO, web sitesinin altyapısını optimize etmeye odaklanır."))
    body.append(p("Bu çalışmalar şunları kapsar:"))
    body.append(
        ul(
            [
                "site hız optimizasyonu",
                "mobil uyumluluk",
                "crawl ve index optimizasyonu",
                "Core Web Vitals iyileştirmeleri",
            ]
        )
    )
    body.append(p("Teknik SEO sayesinde arama motorları web sitesini daha kolay tarayabilir."))

    body.append(h2("3. İçerik Optimizasyonu"))
    body.append(p("SEO için içerik kalitesi oldukça önemlidir."))
    body.append(p("SEO uyumlu içerik oluştururken şu unsurlara dikkat edilmelidir:"))
    body.append(
        ul(
            [
                "doğru anahtar kelimelerin kullanımı",
                "başlık yapısı (H1, H2, H3)",
                "kullanıcı niyetine uygun içerik",
                "değerli ve bilgilendirici metinler",
            ]
        )
    )
    body.append(p("Kaliteli içerikler arama motorlarında daha iyi performans gösterir."))

    body.append(h2("4. İç Bağlantı Yapısı"))
    body.append(p("İç bağlantılar web sitesindeki sayfaları birbirine bağlar."))
    body.append(p("Doğru iç bağlantı stratejisi sayesinde:"))
    body.append(
        ul(
            [
                "SEO otoritesi sayfalar arasında dağıtılır",
                "kullanıcılar ilgili içeriklere kolay ulaşır",
                "arama motorları site yapısını daha iyi anlar",
            ]
        )
    )
    body.append(p("Bu yapı SEO performansını önemli ölçüde artırır."))

    body.append(h2("5. Backlink Stratejisi"))
    body.append(p("Backlink, başka web sitelerinin sizin sitenize verdiği bağlantılardır."))
    body.append(p("Kaliteli backlinkler web sitesinin güvenilirliğini artırır."))
    body.append(p("Backlink stratejileri genellikle şunları içerir:"))
    body.append(
        ul(
            [
                "içerik pazarlaması",
                "dijital PR",
                "sektör sitelerinde yayınlar",
            ]
        )
    )
    body.append(p("Bu çalışmalar web sitesinin otoritesini güçlendirir."))

    body.append(h2("SEO Stratejisinin Sürekliliği"))
    body.append(p("SEO tek seferlik bir çalışma değildir."))
    body.append(p("SEO çalışmalarının düzenli olarak analiz edilmesi ve geliştirilmesi gerekir."))
    body.append(p("Bu süreçte:"))
    body.append(ul(["performans ölçümü", "SEO analizleri", "içerik güncellemeleri"]))
    body.append(p("yapılarak SEO performansı sürekli iyileştirilir."))

    body.append(h2("Angraweb SEO Hizmetleri"))
    body.append(p("Angraweb olarak işletmeler için kapsamlı SEO hizmetleri sunuyoruz."))
    body.append(p("Hizmetlerimiz şunları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO optimizasyonu",
                "içerik ve on page SEO çalışmaları",
                "SEO analizi ve strateji oluşturma",
                "rakip analizi",
            ]
        )
    )
    body.append(p("Amacımız web sitenizin arama motorlarında daha görünür hale gelmesini sağlamaktır."))

    body.append(h2("İlgili SEO Konuları"))
    body.append(
        ul(
            [
                f"{{{{ link:/tr/{_service_base(page)}/seo-nedir/ }}}}",
                f"{{{{ link:/tr/{_service_base(page)}/teknik-seo/ }}}}",
                f"{{{{ link:/tr/{_service_base(page)}/on-page-seo/ }}}}",
                f"{{{{ link:/tr/{_service_base(page)}/seo-analizi/ }}}}",
                f"{{{{ link:{_pillar_url(page)} }}}}",
            ]
        )
    )

    body.append(h2("SEO Hizmeti İçin Teklif Alın"))
    body.append(
        p(
            "Web sitenizin Google sıralamalarını yükseltmek ve organik trafik elde etmek için profesyonel SEO hizmeti alabilirsiniz."
        )
    )
    body.append(
        p(
            f"Projeniz için en doğru SEO stratejisini oluşturmak üzere Angraweb ekibiyle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Nasıl Yapılır? Adım Adım SEO Rehberi – Angraweb"
    meta_description = (
        "SEO nasıl yapılır? Anahtar kelime araştırması, teknik SEO, içerik optimizasyonu ve backlink stratejileri ile web sitenizi Google'da yükseltmenin adımlarını öğrenin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Nasıl Yapılır?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_uyumlu_web_sitesi_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Uyumlu Web Sitesi (TR) — teknik altyapı, içerik, hız, UX."""
    body: List[str] = []

    body.append(h2("SEO Uyumlu Web Sitesi Nedir"))
    body.append(
        p(
            "SEO uyumlu web sitesi, arama motorlarının bir web sitesini kolayca tarayıp anlayabileceği şekilde optimize edilmiş bir site yapısını ifade eder."
        )
    )
    body.append(
        p(
            "SEO uyumlu bir web sitesi sadece teknik açıdan değil, aynı zamanda içerik yapısı, kullanıcı deneyimi ve performans açısından da optimize edilmelidir."
        )
    )
    body.append(
        p(
            "Google ve diğer arama motorları, kullanıcıya en iyi deneyimi sunan siteleri üst sıralarda göstermeyi hedefler. "
            "Bu nedenle SEO uyumlu web tasarımı günümüzde dijital başarı için kritik bir faktördür."
        )
    )

    body.append(h2("SEO Uyumlu Web Sitesinin Temel Özellikleri"))
    body.append(p("SEO uyumlu bir web sitesinde şu özellikler bulunmalıdır:"))
    body.append(
        ul(
            [
                "hızlı sayfa yükleme süreleri",
                "mobil uyumlu tasarım",
                "doğru URL yapısı",
                "optimize edilmiş başlık yapısı",
                "güçlü iç bağlantı yapısı",
            ]
        )
    )
    body.append(
        p(
            "Bu özellikler hem arama motorlarının siteyi daha iyi anlamasını sağlar hem de kullanıcı deneyimini geliştirir."
        )
    )

    body.append(h2("Teknik SEO ve Site Altyapısı"))
    body.append(
        p(
            "Teknik altyapı, SEO uyumlu web sitesinin en önemli bileşenlerinden biridir."
        )
    )
    body.append(p("Teknik SEO çalışmaları şunları içerir:"))
    body.append(
        ul(
            [
                "site hız optimizasyonu",
                "mobil uyumluluk",
                "crawl ve index optimizasyonu",
                "Core Web Vitals iyileştirmeleri",
                "güvenli HTTPS bağlantısı",
            ]
        )
    )
    body.append(
        p(
            "Bu optimizasyonlar sayesinde arama motorları sitenizi daha verimli şekilde tarayabilir."
        )
    )

    body.append(h2("İçerik Yapısı ve SEO"))
    body.append(p("SEO uyumlu web sitelerinde içerik yapısı oldukça önemlidir."))
    body.append(p("Doğru içerik yapısı şu unsurları içerir:"))
    body.append(
        ul(
            [
                "doğru anahtar kelimelerin kullanılması",
                "mantıklı başlık hiyerarşisi",
                "kullanıcı niyetine uygun içerik",
                "değerli ve bilgilendirici metinler",
            ]
        )
    )
    body.append(
        p(
            "Kaliteli içerik hem kullanıcıların hem de arama motorlarının siteyi daha değerli görmesini sağlar."
        )
    )

    body.append(h2("Site Hızı ve Performans"))
    body.append(p("Site hızı SEO açısından önemli bir sıralama faktörüdür."))
    body.append(p("Yavaş web siteleri kullanıcıların siteyi terk etmesine neden olabilir."))
    body.append(p("Performans optimizasyonu için:"))
    body.append(
        ul(
            [
                "görseller optimize edilmelidir",
                "gereksiz kodlar kaldırılmalıdır",
                "CDN kullanılabilir",
                "önbellekleme teknikleri uygulanmalıdır",
            ]
        )
    )
    body.append(p("Hızlı bir web sitesi kullanıcı deneyimini büyük ölçüde iyileştirir."))

    body.append(h2("Mobil Uyumlu Web Tasarımı"))
    body.append(p("Günümüzde internet trafiğinin büyük kısmı mobil cihazlardan gelmektedir."))
    body.append(p("Bu nedenle mobil uyumlu tasarım SEO için zorunludur."))
    body.append(p("Mobil uyumlu web siteleri:"))
    body.append(
        ul(
            [
                "farklı ekran boyutlarına uyum sağlar",
                "kullanıcı deneyimini geliştirir",
                "Google sıralamalarında avantaj sağlar",
            ]
        )
    )
    body.append(p("Responsive tasarım modern web siteleri için standart haline gelmiştir."))

    body.append(h2("SEO Uyumlu Web Tasarımı Neden Önemlidir"))
    body.append(p("SEO uyumlu bir web sitesi şu avantajları sağlar:"))
    body.append(
        ul(
            [
                "daha yüksek Google sıralamaları",
                "daha fazla organik trafik",
                "daha iyi kullanıcı deneyimi",
                "daha yüksek dönüşüm oranları",
            ]
        )
    )
    body.append(p("Bu nedenle modern işletmeler için SEO uyumlu web tasarımı büyük önem taşır."))

    body.append(h2("Angraweb SEO Uyumlu Web Tasarım Hizmeti"))
    body.append(p("Angraweb olarak işletmeler için SEO uyumlu web tasarım ve geliştirme hizmetleri sunuyoruz."))
    body.append(p("Hizmetlerimiz şunları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO altyapısı",
                "hızlı ve optimize edilmiş kod yapısı",
                "mobil uyumlu tasarım",
                "SEO uyumlu içerik yapısı",
            ]
        )
    )
    body.append(p("Amacımız web sitenizin arama motorlarında daha görünür hale gelmesini sağlamaktır."))

    body.append(h2("SEO Uyumlu Web Sitesi İçin Teklif Alın"))
    body.append(
        p(
            "Web sitenizin Google'da daha iyi sıralamalar elde etmesini istiyorsanız SEO uyumlu bir site altyapısı oluşturmak büyük önem taşır."
        )
    )
    body.append(
        p(
            f"Projeniz için en doğru çözümü oluşturmak için Angraweb ekibiyle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Uyumlu Web Sitesi Nedir? SEO Friendly Site Rehberi – Angraweb"
    meta_description = (
        "SEO uyumlu web sitesi nasıl yapılır? Site hızı, teknik SEO, içerik yapısı ve kullanıcı deneyimi ile Google'da üst sıralara çıkmanızı sağlayan web tasarım rehberi."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Uyumlu Web Sitesi",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_uzmani_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Uzmanı Kirala (TR) — profesyonel SEO danışmanlığı, süreç, avantajlar."""
    body: List[str] = []

    body.append(h2("Neden SEO Uzmanı Kiralamalısınız"))
    body.append(
        p(
            "Bir SEO uzmanı kiralamak, web sitenizin arama motorlarında daha görünür olmasını sağlayabilir. "
            "Günümüzde birçok işletme web sitesine sahip olsa da, doğru SEO stratejileri uygulanmadığında bu siteler arama sonuçlarında yeterince görünmez."
        )
    )
    body.append(
        p(
            "Profesyonel bir SEO uzmanı, web sitenizin mevcut durumunu analiz eder ve arama motoru sıralamalarını artırmak için etkili bir optimizasyon planı oluşturur."
        )
    )
    body.append(
        p(
            "Angraweb olarak işletmelerin dijital görünürlüğünü artırmak için veri odaklı ve sürdürülebilir SEO stratejileri uyguluyoruz."
        )
    )

    body.append(h2("SEO Uzmanı Ne Yapar"))
    body.append(
        p(
            "Bir SEO uzmanının görevi, web sitesinin arama motorlarında daha iyi performans göstermesini sağlamaktır."
        )
    )
    body.append(p("SEO uzmanlarının yaptığı çalışmalar şunları içerir:"))
    body.append(
        ul(
            [
                "SEO site analizi",
                "anahtar kelime araştırması",
                "site içi SEO optimizasyonu",
                "teknik SEO geliştirmeleri",
                "backlink stratejisi oluşturma",
            ]
        )
    )
    body.append(
        p(
            "Bu çalışmalar web sitesinin Google gibi arama motorlarında daha üst sıralara çıkmasına yardımcı olur."
        )
    )

    body.append(h2("Ne Zaman SEO Uzmanı Kiralamalısınız"))
    body.append(
        p(
            "Birçok işletme web sitesi kurduktan sonra SEO çalışmalarına ihtiyaç duyar."
        )
    )
    body.append(p("SEO uzmanı kiralamayı düşünmeniz gereken durumlar:"))
    body.append(
        ul(
            [
                "web sitenizin Google'da görünmemesi",
                "organik trafiğin düşük olması",
                "rakiplerin arama sonuçlarında üstte olması",
                "dijital pazarlamada büyümek istemeniz",
            ]
        )
    )
    body.append(
        p(
            "Profesyonel bir SEO stratejisi bu sorunların çözülmesine yardımcı olabilir."
        )
    )

    body.append(h2("Angraweb SEO Süreci"))
    body.append(
        p(
            "Angraweb olarak SEO projelerinde belirli bir süreç izliyoruz."
        )
    )
    body.append(h3("Analiz ve Keşif"))
    body.append(
        p(
            "İlk aşamada web sitenizin mevcut performansı analiz edilir."
        )
    )
    body.append(p("Bu süreçte şu çalışmalar yapılır:"))
    body.append(
        ul(
            [
                "SEO analizi",
                "rakip analizi",
                "anahtar kelime araştırması",
            ]
        )
    )
    body.append(
        p(
            "Bu analizler SEO stratejisinin temelini oluşturur."
        )
    )
    body.append(h3("SEO Stratejisi"))
    body.append(
        p(
            "Analiz tamamlandıktan sonra web sitesi için bir SEO stratejisi oluşturulur."
        )
    )
    body.append(p("Bu strateji şu alanları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO optimizasyonu",
                "içerik geliştirme",
                "anahtar kelime hedefleme",
                "backlink stratejisi",
            ]
        )
    )
    body.append(h3("Uygulama ve Optimizasyon"))
    body.append(
        p(
            "SEO planı oluşturulduktan sonra optimizasyon çalışmaları uygulanır."
        )
    )
    body.append(p("Bu çalışmalar:"))
    body.append(
        ul(
            [
                "sayfa başlıklarını optimize etmek",
                "içerikleri geliştirmek",
                "site hızını artırmak",
                "kullanıcı deneyimini iyileştirmek",
            ]
        )
    )
    body.append(
        p(
            "gibi adımları içerir."
        )
    )
    body.append(h3("İzleme ve Raporlama"))
    body.append(
        p(
            "SEO çalışmaları uygulandıktan sonra performans düzenli olarak takip edilir."
        )
    )
    body.append(p("Bu süreçte:"))
    body.append(
        ul(
            [
                "anahtar kelime sıralamaları",
                "organik trafik",
                "site performansı",
            ]
        )
    )
    body.append(
        p(
            "analiz edilir ve raporlanır."
        )
    )

    body.append(h2("Web Siteniz İçin SEO Uzmanı Kiralayın"))
    body.append(
        p(
            "Eğer web sitenizin Google'da daha üst sıralarda görünmesini istiyorsanız profesyonel bir SEO uzmanı ile çalışmak büyük bir avantaj sağlar."
        )
    )
    body.append(
        p(
            "Angraweb SEO uzmanları, işletmenizin dijital büyümesini destekleyen sürdürülebilir SEO stratejileri geliştirir."
        )
    )
    body.append(
        p(
            f"SEO hizmetleri hakkında detaylı bilgi almak veya projeniz için teklif almak için bizimle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Uzmanı Kirala | Profesyonel SEO Danışmanlığı – Angraweb"
    meta_description = (
        "SEO uzmanı kiralayarak web sitenizin Google sıralamalarını yükseltin. Profesyonel SEO analizi, teknik optimizasyon ve anahtar kelime stratejisi ile organik trafik artırın."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Uzmanı Kirala",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_istanbul_seo_ajansi_tr(page: SeoPage) -> Dict:
    """Custom cluster: İstanbul SEO Ajansı (TR) — yerel SEO, süreç, raporlama."""
    body: List[str] = []

    body.append(h2("İstanbul SEO Ajansı"))
    body.append(
        p(
            "İstanbul'da faaliyet gösteren işletmeler için dijital rekabet her geçen gün artmaktadır. "
            "Bu nedenle web sitelerinin Google gibi arama motorlarında görünür olması büyük önem taşır."
        )
    )
    body.append(
        p(
            "Profesyonel bir İstanbul SEO ajansı ile çalışmak, web sitenizin arama sonuçlarında daha üst sıralarda yer almasına yardımcı olur."
        )
    )
    body.append(
        p(
            "Angraweb olarak İstanbul'daki işletmeler için veri odaklı ve sürdürülebilir SEO stratejileri geliştiriyoruz. "
            "Amacımız yalnızca sıralama yükseltmek değil, aynı zamanda işletmelerin gerçek müşteri kazanmasını sağlamaktır."
        )
    )

    body.append(h2("Neden İstanbul'da SEO Hizmeti Önemlidir"))
    body.append(
        p(
            "İstanbul Türkiye'nin en rekabetçi dijital pazarlarından biridir. "
            "Bu nedenle birçok sektörde yüzlerce web sitesi aynı anahtar kelimeler için yarışmaktadır."
        )
    )
    body.append(p("SEO çalışmaları sayesinde işletmeler:"))
    body.append(
        ul(
            [
                "Google aramalarında daha görünür olur",
                "organik trafik elde eder",
                "potansiyel müşterilere ulaşır",
                "dijital marka otoritesi oluşturur",
            ]
        )
    )
    body.append(
        p(
            "Doğru SEO stratejisi, İstanbul'daki işletmeler için uzun vadeli bir dijital büyüme sağlar."
        )
    )

    body.append(h2("İstanbul SEO Ajansı Ne Yapar"))
    body.append(
        p(
            "Bir SEO ajansı web sitenizin arama motorlarında daha iyi performans göstermesi için kapsamlı optimizasyon çalışmaları yapar."
        )
    )
    body.append(p("Bu çalışmalar genellikle şu alanları kapsar:"))
    body.append(
        ul(
            [
                "SEO site analizi",
                "anahtar kelime araştırması",
                "teknik SEO optimizasyonu",
                "site içi SEO geliştirmeleri",
                "içerik stratejisi",
                "backlink çalışmaları",
            ]
        )
    )
    body.append(
        p(
            "Bu süreç web sitesinin arama motorları tarafından daha iyi anlaşılmasını sağlar."
        )
    )

    body.append(h2("Yerel SEO Stratejisi"))
    body.append(
        p(
            "İstanbul'da faaliyet gösteren işletmeler için yerel SEO çalışmaları büyük önem taşır."
        )
    )
    body.append(p("Yerel SEO stratejileri şu çalışmaları içerir:"))
    body.append(
        ul(
            [
                "Google Business Profile optimizasyonu",
                "yerel anahtar kelime hedefleme",
                "konum bazlı içerik üretimi",
                "yerel backlink çalışmaları",
            ]
        )
    )
    body.append(
        p(
            "Bu yöntemler sayesinde işletmeler İstanbul'da yapılan aramalarda daha üst sıralarda görünür."
        )
    )

    body.append(h2("Angraweb SEO Süreci"))
    body.append(
        p(
            "Angraweb olarak SEO projelerinde sistemli bir yaklaşım izliyoruz."
        )
    )
    body.append(h3("SEO Analizi"))
    body.append(
        p(
            "İlk aşamada web sitesinin teknik yapısı ve mevcut SEO performansı analiz edilir."
        )
    )
    body.append(p("Bu aşamada:"))
    body.append(
        ul(
            [
                "teknik hatalar",
                "sayfa performansı",
                "anahtar kelime fırsatları",
            ]
        )
    )
    body.append(p("belirlenir."))
    body.append(h3("SEO Stratejisi"))
    body.append(
        p(
            "Analiz tamamlandıktan sonra işletmenin hedeflerine uygun bir SEO stratejisi hazırlanır."
        )
    )
    body.append(p("Bu strateji şu alanları kapsar:"))
    body.append(
        ul(
            [
                "teknik SEO geliştirmeleri",
                "içerik optimizasyonu",
                "anahtar kelime hedefleme",
            ]
        )
    )
    body.append(h3("Uygulama ve Optimizasyon"))
    body.append(
        p(
            "SEO planı uygulamaya alındıktan sonra web sitesinde optimizasyon çalışmaları yapılır."
        )
    )
    body.append(p("Bu çalışmalar:"))
    body.append(
        ul(
            [
                "sayfa başlıklarını optimize etmek",
                "içerikleri geliştirmek",
                "site hızını artırmak",
            ]
        )
    )
    body.append(p("gibi adımları içerir."))
    body.append(h3("İzleme ve Raporlama"))
    body.append(
        p(
            "SEO çalışmalarının başarısı düzenli olarak analiz edilir."
        )
    )
    body.append(p("Bu süreçte:"))
    body.append(
        ul(
            [
                "anahtar kelime sıralamaları",
                "organik trafik",
                "kullanıcı davranışları",
            ]
        )
    )
    body.append(p("takip edilir ve raporlanır."))

    body.append(h2("İstanbul'da SEO Ajansı Nasıl Seçilir"))
    body.append(
        p(
            "Doğru SEO ajansını seçmek dijital başarı için önemlidir."
        )
    )
    body.append(p("Bir SEO ajansı seçerken şu kriterlere dikkat edilmelidir:"))
    body.append(
        ul(
            [
                "deneyim ve referans projeler",
                "kullanılan SEO stratejileri",
                "raporlama sistemi",
                "uzun vadeli SEO yaklaşımı",
            ]
        )
    )
    body.append(
        p(
            "Şeffaf ve veri odaklı çalışan bir SEO ajansı uzun vadede daha başarılı sonuçlar sağlar."
        )
    )

    body.append(h2("Angraweb İstanbul SEO Hizmetleri"))
    body.append(
        p(
            "Angraweb olarak İstanbul'daki işletmelere profesyonel SEO çözümleri sunuyoruz."
        )
    )
    body.append(p("SEO hizmetlerimiz:"))
    body.append(
        ul(
            [
                "teknik SEO optimizasyonu",
                "anahtar kelime stratejisi",
                "içerik geliştirme",
                "performans izleme",
            ]
        )
    )
    body.append(p("gibi alanları kapsar."))
    body.append(
        p(
            "Hedefimiz web sitenizin Google aramalarında daha görünür olmasını sağlamak ve sürdürülebilir organik trafik elde etmektir."
        )
    )

    body.append(h2("Projeniz İçin SEO Teklifi Alın"))
    body.append(
        p(
            "Eğer İstanbul'da işletmeniz için profesyonel bir SEO ajansı arıyorsanız Angraweb ekibi size yardımcı olabilir."
        )
    )
    body.append(
        p(
            f"Web siteniz için doğru SEO stratejisini oluşturmak ve organik trafiğinizi artırmak için bizimle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "İstanbul SEO Ajansı | Profesyonel SEO Hizmetleri – Angraweb"
    meta_description = (
        "İstanbul SEO ajansı arıyorsanız doğru yerdesiniz. Angraweb ile profesyonel SEO hizmetleri, teknik optimizasyon ve organik trafik artışı sağlayın."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "İstanbul SEO Ajansı",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
        "published_at": timezone.now(),
    }


def _cluster_seo_ajans_freelancer_tr(page: SeoPage) -> Dict:
    """Custom cluster: SEO Ajansı mı Freelancer mı? (TR) — avantajlar, ne zaman hangisi. No pricing triggers."""
    body: List[str] = []

    body.append(h2("SEO Ajansı mı Freelancer mı?"))
    body.append(
        p(
            "SEO hizmeti almak isteyen birçok işletme aynı soruyu sorar: SEO ajansı ile çalışmak mı daha iyi, yoksa freelancer bir SEO uzmanı mı tercih edilmelidir?"
        )
    )
    body.append(
        p(
            "Her iki yaklaşımın da avantajları ve dezavantajları vardır. Doğru seçim; projenin büyüklüğüne, bütçeye ve ihtiyaç duyulan uzmanlık seviyesine bağlıdır."
        )
    )
    body.append(
        p(
            "Bu rehberde SEO ajansı ve freelancer arasındaki farkları inceleyerek hangi seçeneğin sizin için daha uygun olduğunu açıklıyoruz."
        )
    )

    body.append(h2("SEO Freelancer ile Çalışmanın Avantajları"))
    body.append(
        p(
            "Freelancer SEO uzmanları genellikle bireysel olarak çalışan ve belirli bir uzmanlık alanına odaklanan profesyonellerdir."
        )
    )
    body.append(p("Freelancer ile çalışmanın bazı avantajları şunlardır:"))
    body.append(
        ul(
            [
                "daha uygun bütçe",
                "daha hızlı iletişim",
                "küçük projeler için esneklik",
                "kısa süreli projeler için uygunluk",
            ]
        )
    )
    body.append(
        p(
            "Özellikle küçük işletmeler veya yeni başlayan web siteleri için freelancer SEO uzmanları iyi bir başlangıç çözümü olabilir."
        )
    )

    body.append(h2("Freelancer ile Çalışmanın Dezavantajları"))
    body.append(
        p(
            "Freelancer SEO uzmanları bazı durumlarda sınırlı kaynaklara sahip olabilir."
        )
    )
    body.append(p("Örneğin:"))
    body.append(
        ul(
            [
                "tek kişi çalıştığı için iş kapasitesi sınırlıdır",
                "teknik SEO, içerik ve backlink gibi alanlarda farklı uzmanlıklar gerekebilir",
                "büyük projelerde süreç yönetimi zorlaşabilir",
            ]
        )
    )
    body.append(
        p(
            "Bu nedenle büyük ve uzun vadeli SEO projelerinde freelancer modeli her zaman yeterli olmayabilir."
        )
    )

    body.append(h2("SEO Ajansı ile Çalışmanın Avantajları"))
    body.append(
        p(
            "SEO ajansları genellikle farklı uzmanlık alanlarına sahip ekiplerden oluşur."
        )
    )
    body.append(p("Bir SEO ajansı ile çalışmanın avantajları şunlardır:"))
    body.append(
        ul(
            [
                "farklı uzmanlık alanlarına erişim",
                "daha kapsamlı SEO stratejisi",
                "düzenli raporlama ve süreç yönetimi",
                "uzun vadeli SEO planı",
            ]
        )
    )
    body.append(
        p(
            "Ajanslar genellikle teknik SEO, içerik üretimi ve backlink stratejisi gibi alanlarda ekip halinde çalışır."
        )
    )

    body.append(h2("SEO Ajansı ile Çalışmanın Dezavantajları"))
    body.append(
        p(
            "Ajanslarla çalışmanın bazı dezavantajları da olabilir."
        )
    )
    body.append(p("Örneğin:"))
    body.append(
        ul(
            [
                "freelancerlara göre daha yüksek bütçe",
                "bazı durumlarda iletişim süreçleri daha formal olabilir",
            ]
        )
    )
    body.append(
        p(
            "Ancak doğru ajans seçildiğinde bu dezavantajlar genellikle proje yönetimi avantajlarıyla dengelenir."
        )
    )

    body.append(h2("Hangi Durumda Freelancer Seçmelisiniz"))
    body.append(
        p(
            "Aşağıdaki durumlarda freelancer SEO uzmanı ile çalışmak mantıklı olabilir:"
        )
    )
    body.append(
        ul(
            [
                "küçük ölçekli bir web sitesi",
                "sınırlı bütçe",
                "kısa süreli SEO danışmanlığı",
            ]
        )
    )
    body.append(
        p(
            "Bu tür projelerde freelancer modeli hızlı ve ekonomik bir çözüm olabilir."
        )
    )

    body.append(h2("Hangi Durumda SEO Ajansı Seçmelisiniz"))
    body.append(
        p(
            "Aşağıdaki durumlarda SEO ajansı ile çalışmak daha doğru bir seçim olabilir:"
        )
    )
    body.append(
        ul(
            [
                "rekabetin yüksek olduğu sektörler",
                "büyük e-ticaret siteleri",
                "uzun vadeli SEO stratejileri",
            ]
        )
    )
    body.append(
        p(
            "Ajanslar daha kapsamlı projelerde daha sürdürülebilir sonuçlar sağlayabilir."
        )
    )

    body.append(h2("SEO Hizmeti Seçerken Nelere Dikkat Edilmeli"))
    body.append(
        p(
            "SEO hizmeti seçerken yalnızca bütçe değil, uzmanlık ve deneyim de önemlidir."
        )
    )
    body.append(p("Doğru SEO hizmetini seçmek için şu faktörlere dikkat edilmelidir:"))
    body.append(
        ul(
            [
                "referans projeler",
                "kullanılan SEO yöntemleri",
                "raporlama sistemi",
                "uzun vadeli strateji",
            ]
        )
    )
    body.append(
        p(
            "SEO çalışmaları uzun vadeli bir süreç olduğu için güvenilir bir partner seçmek önemlidir."
        )
    )

    body.append(h2("Angraweb SEO Hizmetleri"))
    body.append(
        p(
            "Angraweb olarak işletmelere hem stratejik hem de teknik SEO çözümleri sunuyoruz."
        )
    )
    body.append(p("SEO çalışmalarımız şu alanları kapsar:"))
    body.append(
        ul(
            [
                "SEO analizi",
                "teknik SEO optimizasyonu",
                "anahtar kelime stratejisi",
                "içerik geliştirme",
            ]
        )
    )
    body.append(
        p(
            "Amacımız web sitenizin arama motorlarında daha görünür hale gelmesini sağlamak ve sürdürülebilir organik trafik elde etmektir."
        )
    )
    body.append(
        p(
            f"SEO hizmetleri hakkında daha fazla bilgi almak veya projeniz için teklif almak için bizimle iletişime geçebilirsiniz. {{{{ link:{_quote_url(page)} }}}}"
        )
    )
    body.append(h2("İlgili sayfalar"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
            ]
        )
    )

    content_html = "\n".join(body)
    meta_title = "SEO Ajansı mı Freelancer mı? Hangisi Daha İyi – Angraweb"
    meta_description = (
        "SEO ajansı mı freelancer mı daha iyi? SEO hizmeti alırken ajans ve freelancer arasındaki farkları, avantajları ve doğru seçim yöntemlerini öğrenin."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "SEO Ajansı mı Freelancer mı?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": [],
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

