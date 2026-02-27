from __future__ import annotations

from django.urls import path, register_converter

from .converters import EnServiceBaseConverter
from .models import SeoPage
from .views import seo_page_view

register_converter(EnServiceBaseConverter, "en_service")

app_name = "seo_pages_en"

urlpatterns = [
    path(
        "<en_service:service_base>/",
        seo_page_view,
        {"language": "en", "page_type": SeoPage.TYPE_PILLAR, "slug": ""},
        name="pillar",
    ),
    path(
        "<en_service:service_base>/pricing/",
        seo_page_view,
        {"language": "en", "page_type": SeoPage.TYPE_PRICING, "slug": "pricing"},
        name="pricing",
    ),
    path(
        "<en_service:service_base>/guide/",
        seo_page_view,
        {"language": "en", "page_type": SeoPage.TYPE_GUIDE, "slug": "guide"},
        name="guide",
    ),
    path(
        "<en_service:service_base>/get-quote/",
        seo_page_view,
        {"language": "en", "page_type": SeoPage.TYPE_QUOTE, "slug": "get-quote"},
        name="quote",
    ),
    path(
        "<en_service:service_base>/<slug:slug>/",
        seo_page_view,
        {"language": "en", "page_type": SeoPage.TYPE_CLUSTER},
        name="cluster",
    ),
]

