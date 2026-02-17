"""
Middleware برای اطمینان از فعال شدن زبان از session/cookie
و نمایش صفحه نگهداری (Bakım Modu)
و مدیریت انقضای session
"""
from django.conf import settings
from django.shortcuts import render
from django.utils import translation
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta


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
    و ترجمه‌ها به درستی لود می‌شوند
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
        
        # اگر زبان پیدا نشد، از زبان پیش‌فرض استفاده کن
        if not lang or lang not in ['tr', 'en', 'fa', 'ar']:
            lang = settings.LANGUAGE_CODE
        
        # حتماً زبان را activate کن تا ترجمه‌ها لود شوند
        translation.activate(lang)
        
        # اگر زبان در session نیست، آن را ذخیره کن تا دفعه بعد استفاده شود
        if hasattr(request, 'session') and request.session.get(session_key) != lang:
            request.session[session_key] = lang
            request.session.modified = True
        
        # حالا view را اجرا کن
        response = self.get_response(request)
        
        return response


class SessionExpiryMiddleware:
    """
    چک می‌کند که session منقضی شده باشد یا نه.
    اگر session منقضی شده باشد و کاربر لاگین کرده باشد، او را logout می‌کند.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر کاربر لاگین کرده باشد
        if request.user.is_authenticated:
            # زمان آخرین فعالیت را از session بخوان
            last_activity = request.session.get('last_activity')
            session_age = getattr(settings, 'SESSION_COOKIE_AGE', 7200)  # پیش‌فرض 2 ساعت
            
            if last_activity:
                try:
                    # اگر string است، تبدیل به datetime کن
                    if isinstance(last_activity, str):
                        from datetime import datetime
                        last_activity = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                        if timezone.is_naive(last_activity):
                            last_activity = timezone.make_aware(last_activity)
                    
                    # محاسبه زمان گذشته از آخرین فعالیت
                    time_passed = (timezone.now() - last_activity).total_seconds()
                    
                    # اگر زمان گذشته بیشتر از session_age باشد، کاربر را logout کن
                    if time_passed > session_age:
                        logout(request)
                        request.session.flush()  # پاک کردن session
                        # بعد از logout، ادامه نده
                        response = self.get_response(request)
                        return response
                except (ValueError, TypeError, AttributeError):
                    # اگر خطا در parsing بود، last_activity را reset کن
                    pass
            
            # به‌روزرسانی last_activity در هر درخواست
            # Store as ISO string for JSON serialization
            request.session['last_activity'] = timezone.now().isoformat()
        else:
            # اگر کاربر لاگین نکرده باشد، last_activity را پاک کن
            if 'last_activity' in request.session:
                del request.session['last_activity']
        
        response = self.get_response(request)
        return response
