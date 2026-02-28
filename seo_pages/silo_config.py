from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .models import SeoPage


SERVICE_SILO_MAP: Dict[str, dict] = {
    # ------------------------------------------------------------
    # WEB DESIGN / WEB TASARIM
    # ------------------------------------------------------------
    "web-design": {
        "tr": {
            "name": "Web Tasarım",
            "base_path": "web-tasarim",
            "clusters": [
                "kurumsal-web-sitesi",
                "kurumsal-web-sitesi-yaptirmak",
                "istanbul",
                "ozel-yazilim-web-sitesi",
                "django-web-gelistirme",
                "profesyonel-web-tasarim",
                "web-tasarim-sirketi",
                "web-tasarim-freelancer",
                "web-developer-istanbul",
                "ozel-yazilim-vs-hazir-site",
                "django-vs-php",
                "ajans-mi-freelancer-mi",
            ],
        },
        "en": {
            "name": "Web Design",
            "base_path": "web-design",
            "clusters": [
                "web-design-services",
                "corporate-website-development",
                "web-design-company-istanbul",
                "web-design-agency",
                "django-web-development",
                "custom-web-development",
                "web-development-company",
                "hire-web-developer",
                "what-is-web-design",
                "how-to-build-a-website",
                "custom-website-vs-template",
                "django-vs-php",
            ],
        },
    },
    # ------------------------------------------------------------
    # MOBILE APP DEVELOPMENT / MOBİL UYGULAMA GELİŞTİRME
    # ------------------------------------------------------------
    "mobile-app-development": {
        "tr": {
            "name": "Mobil Uygulama Geliştirme",
            "base_path": "mobil-uygulama-gelistirme",
            "clusters": [
                "react-native",
                "android",
                "ios",
                "ozel-mobil-uygulama",
                "istanbul",
                "mobil-uygulama-nedir",
                "mobil-uygulama-nasil-yapilir",
                "mobil-uygulama-freelancer",
                "react-native-vs-native",
                "android-vs-ios",
            ],
        },
        "en": {
            "name": "Mobile App Development",
            "base_path": "mobile-app-development",
            "clusters": [
                "react-native-app-development",
                "android-app-development",
                "ios-app-development",
                "custom-mobile-app-development",
                "mobile-app-development-company",
                "what-is-mobile-app-development",
                "hire-mobile-app-developer",
                "react-native-vs-native",
                "cross-platform-vs-native",
                "mobile-app-development-cost",
            ],
        },
    },
    # ------------------------------------------------------------
    # ECOMMERCE DEVELOPMENT / E-TİCARET GELİŞTİRME
    # ------------------------------------------------------------
    "ecommerce-development": {
        "tr": {
            "name": "E‑Ticaret Geliştirme",
            "base_path": "e-ticaret-gelistirme",
            "clusters": [
                "e-ticaret-sitesi",
                "e-ticaret-yazilimi",
                "ozel-e-ticaret-yazilimi",
                "b2b",
                "b2c",
                "e-ticaret-yazilim-firmasi",
                "e-ticaret-sitesi-yaptirmak",
                "e-ticaret-nedir",
                "e-ticaret-sitesi-nasil-kurulur",
                "ozel-yazilim-vs-hazir-altyapi",
            ],
        },
        "en": {
            "name": "Ecommerce Development",
            "base_path": "ecommerce-development",
            "clusters": [
                "custom-ecommerce-development",
                "ecommerce-development-company",
                "ecommerce-platform-development",
                "b2b-ecommerce-development",
                "b2c-ecommerce-website",
                "what-is-ecommerce",
                "ecommerce-website-guide",
                "ecommerce-website-cost",
                "ecommerce-pricing",
                "custom-vs-template-ecommerce",
            ],
        },
    },
    # ------------------------------------------------------------
    # SEO SERVICES / SEO HİZMETLERİ
    # ------------------------------------------------------------
    "seo-services": {
        "tr": {
            "name": "SEO Hizmetleri",
            "base_path": "seo-hizmetleri",
            "clusters": [
                "seo-danismanligi",
                "teknik-seo",
                "on-page-seo",
                "seo-analizi",
                "istanbul-seo-ajansi",
                "seo-uzmani",
                "seo-nedir",
                "seo-nasil-yapilir",
                "seo-uyumlu-web-sitesi",
                "ajans-mi-freelancer-mi",
            ],
        },
        "en": {
            "name": "SEO Services",
            "base_path": "seo-services",
            "clusters": [
                "technical-seo-services",
                "on-page-seo-services",
                "seo-consultancy",
                "seo-pricing",
                "seo-cost",
                "what-is-seo",
                "how-seo-works",
                "hire-seo-expert",
                "seo-audit",
                "seo-for-django-sites",
            ],
        },
    },
    # ------------------------------------------------------------
    # HOSTING & DOMAIN
    # ------------------------------------------------------------
    "hosting-domain": {
        "tr": {
            "name": "Hosting & Domain",
            "base_path": "hosting-domain",
            "clusters": [
                "hosting-hizmeti",
                "vps-hosting",
                "ozel-sunucu-kiralama",
                "bulut-sunucu",
                "django-deployment",
                "domain-satin-al",
                "ssl-sertifikasi",
                "linux-sunucu-kurulumu",
                "web-hosting-fiyatlari",
                "vps-fiyatlari",
            ],
        },
        "en": {
            "name": "Hosting & Domain",
            "base_path": "hosting-domain",
            "clusters": [
                "web-hosting-services",
                "vps-hosting",
                "dedicated-server-hosting",
                "cloud-hosting",
                "django-hosting",
                "domain-registration",
                "ssl-certificate",
                "linux-server-setup",
                "web-hosting-pricing",
                "vps-hosting-cost",
            ],
        },
    },
    # ------------------------------------------------------------
    # UI/UX DESIGN
    # ------------------------------------------------------------
    "ui-ux-design": {
        "tr": {
            "name": "UI/UX Tasarım",
            "base_path": "ui-ux-tasarim",
            "clusters": [
                "ui-ux-nedir",
                "kullanici-deneyimi-tasarimi",
                "kullanici-arayuzu-tasarimi",
                "ui-ux-tasarim-hizmeti",
                "mobil-uygulama-arayuz-tasarimi",
                "ux-arastirmasi",
                "figma-tasarim",
                "wireframe-tasarimi",
                "prototype-tasarimi",
                "ui-ux-tasarim-fiyatlari",
            ],
        },
        "en": {
            "name": "UI/UX Design",
            "base_path": "ui-ux-design",
            "clusters": [
                "ui-ux-design-services",
                "user-experience-design",
                "user-interface-design",
                "what-is-ui-ux",
                "figma-design",
                "wireframe-design",
                "prototype-design",
                "mobile-app-ui-design",
                "ui-ux-pricing",
                "ux-research",
            ],
        },
    },
}


def get_service_bases(language: str) -> List[str]:
    if language not in ("tr", "en"):
        return []
    return sorted({SERVICE_SILO_MAP[k][language]["base_path"] for k in SERVICE_SILO_MAP.keys()})


def get_mirrored_slug(service_key: str, page_type: str, from_language: str, from_slug: str) -> Optional[str]:
    """
    Return the mirrored slug in the other language for hreflang.

    - Pillar: "" <-> ""
    - Pricing/Guide/Quote: fixed slugs
    - Cluster: mapped by the configured lists order
    """

    if service_key not in SERVICE_SILO_MAP:
        return None
    if from_language not in ("tr", "en"):
        return None
    to_language = "en" if from_language == "tr" else "tr"

    if page_type == SeoPage.TYPE_PILLAR:
        return ""
    if page_type == SeoPage.TYPE_PRICING:
        return "pricing" if to_language == "en" else "fiyatlar"
    if page_type == SeoPage.TYPE_GUIDE:
        return "guide" if to_language == "en" else "rehber"
    if page_type == SeoPage.TYPE_QUOTE:
        return "get-quote" if to_language == "en" else "teklif-al"

    if page_type != SeoPage.TYPE_CLUSTER:
        return None

    from_clusters = SERVICE_SILO_MAP[service_key][from_language]["clusters"]
    to_clusters = SERVICE_SILO_MAP[service_key][to_language]["clusters"]
    try:
        idx = from_clusters.index(from_slug)
    except ValueError:
        return None
    if idx < 0 or idx >= len(to_clusters):
        return None
    return to_clusters[idx]


def iter_all_seed_pages() -> List[Tuple[str, str, str]]:
    """
    Returns tuples: (language, service_key, slug_path)
    This is used by the seed migration.
    """

    rows: List[Tuple[str, str, str]] = []
    for service_key, cfg in SERVICE_SILO_MAP.items():
        for language in ("tr", "en"):
            # Pillar / Pricing / Guide / Quote
            rows.append((language, service_key, ""))  # pillar
            rows.append((language, service_key, "fiyatlar" if language == "tr" else "pricing"))
            rows.append((language, service_key, "rehber" if language == "tr" else "guide"))
            rows.append((language, service_key, "teklif-al" if language == "tr" else "get-quote"))
            # Clusters
            for slug in cfg[language]["clusters"]:
                rows.append((language, service_key, slug))
    return rows

