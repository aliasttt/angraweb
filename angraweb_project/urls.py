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
from main.views import set_language, redirect_to_default_language, sitemap_xml, robots_txt
from insights.views_admin import admin_dashboard as admin_dashboard_view
from insights.views_admin import seo_health_dashboard as seo_health_dashboard_view

# Non-prefixed URLs
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('lang/<str:lang_code>/', set_language, name='switch_lang'),
    path('admin/insights/seo-health/', seo_health_dashboard_view),
    path('admin/insights/', admin_dashboard_view),
    path('admin/', admin.site.urls),
    path('insights/', include('insights.urls')),
    path('sitemap.xml', sitemap_xml),
    path('robots.txt', robots_txt),
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
