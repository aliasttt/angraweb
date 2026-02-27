from __future__ import annotations

from django.urls import path, register_converter

from .converters import TrServiceBaseConverter
from .models import SeoPage
from .views import seo_page_view

register_converter(TrServiceBaseConverter, "tr_service")

app_name = "seo_pages_tr"

urlpatterns = [
    path(
        "<tr_service:service_base>/",
        seo_page_view,
        {"language": "tr", "page_type": SeoPage.TYPE_PILLAR, "slug": ""},
        name="pillar",
    ),
    path(
        "<tr_service:service_base>/fiyatlar/",
        seo_page_view,
        {"language": "tr", "page_type": SeoPage.TYPE_PRICING, "slug": "fiyatlar"},
        name="pricing",
    ),
    path(
        "<tr_service:service_base>/rehber/",
        seo_page_view,
        {"language": "tr", "page_type": SeoPage.TYPE_GUIDE, "slug": "rehber"},
        name="guide",
    ),
    path(
        "<tr_service:service_base>/teklif-al/",
        seo_page_view,
        {"language": "tr", "page_type": SeoPage.TYPE_QUOTE, "slug": "teklif-al"},
        name="quote",
    ),
    path(
        "<tr_service:service_base>/<slug:slug>/",
        seo_page_view,
        {"language": "tr", "page_type": SeoPage.TYPE_CLUSTER},
        name="cluster",
    ),
]

