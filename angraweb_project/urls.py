"""
URL configuration for angraweb_project project.

- Non-prefixed: i18n, admin, insights, static/media.
- Language-prefixed (tr/en): main app via i18n_patterns; both /tr/ and /en/ explicitly.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from main.views import set_language, redirect_to_default_language, robots_txt, yandex_verification, debug_static
from insights.views_admin import admin_dashboard as admin_dashboard_view
from insights.views_admin import seo_health_dashboard as seo_health_dashboard_view
from seo_pages.sitemap import sitemaps as seo_sitemaps

# Non-prefixed URLs
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('lang/<str:lang_code>/', set_language, name='switch_lang'),
    path('admin/insights/seo-health/', seo_health_dashboard_view),
    path('admin/insights/', admin_dashboard_view),
    path('admin/', admin.site.urls),
    path('insights/', include('insights.urls')),
    # Explicit language hubs for service silos (avoid mixed-slug routes under i18n_patterns)
    path('tr/', include('seo_pages.urls_tr')),
    path('en/', include('seo_pages.urls_en')),
    # SEO-first sitemap index + per-language sitemaps (TR/EN are separate graphs)
    path('sitemap.xml', sitemap_views.index, {"sitemaps": seo_sitemaps, "sitemap_url_name": "sitemap-section"}),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {"sitemaps": seo_sitemaps}, name="sitemap-section"),
    path('robots.txt', robots_txt),
    path('yandex_cdb21588d18ce4cc.html', yandex_verification),
    path('debug-static/', debug_static),
    path('', redirect_to_default_language),
]

# Language-prefixed: both /tr/ and /en/ (prefix_default_language=True)
urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
