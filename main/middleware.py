"""
Middleware برای اطمینان از فعال شدن زبان از session/cookie
و نمایش صفحه نگهداری (Bakım Modu)
"""
from django.conf import settings
from django.shortcuts import render
from django.utils import translation


class MaintenanceMiddleware:
    """
    وقتی MAINTENANCE_MODE فعال است، صفحه نگهداری به ترکی نمایش می‌دهد.
    مسیرهای /static/ و /media/ و (اختیاری) ادمین از فیلتر خارج می‌شوند.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, 'MAINTENANCE_MODE', False):
            return self.get_response(request)
        path = request.path_info.lstrip('/')
        if path.startswith('static/') or path.startswith('media/') or path.startswith('admin/'):
            return self.get_response(request)
        if getattr(settings, 'MAINTENANCE_BYPASS_STAFF', True) and getattr(request.user, 'is_staff', False):
            return self.get_response(request)
        return render(request, 'main/maintenance.html', status=503)


class LanguageActivationMiddleware:
    """
    بعد از LocaleMiddleware اجرا می‌شود و مطمئن می‌شود که زبان از session/cookie activate شده
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # قبل از اجرای view، زبان را از session/cookie بخوان و activate کن
        # (LocaleMiddleware قبلاً اجرا شده و زبان را از session خوانده، اما ما دوباره چک می‌کنیم)
        session_key = getattr(settings, 'LANGUAGE_SESSION_KEY', '_language')
        lang = None
        
        # از session بخوان
        if hasattr(request, 'session'):
            lang = request.session.get(session_key)
        
        # اگر session نبود، از cookie بخوان
        if not lang:
            cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
            lang = request.COOKIES.get(cookie_name)
        
        # اگر زبان پیدا شد و معتبر است، activate کن (قبل از اجرای view)
        if lang and lang in ['tr', 'en', 'fa', 'ar']:
            translation.activate(lang)
        
        # حالا view را اجرا کن
        response = self.get_response(request)
        
        return response
