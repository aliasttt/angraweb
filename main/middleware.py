"""
Middleware برای اطمینان از فعال شدن زبان از session/cookie
"""
from django.conf import settings
from django.utils import translation


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
