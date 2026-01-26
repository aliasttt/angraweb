# دستورالعمل Migration و راه‌اندازی

## 📋 تغییرات انجام شده

### ✅ تکمیل شده:
1. ✅ امنیت Production - Environment Variables
2. ✅ Meta Tags کامل - Open Graph و Twitter Cards
3. ✅ Schema Markup - JSON-LD
4. ✅ صفحات 404 و 500 سفارشی
5. ✅ Rate Limiting برای فرم‌ها
6. ✅ سیستم Blog کامل
7. ✅ سیستم Testimonials
8. ✅ FAQ Page
9. ✅ Newsletter System
10. ✅ Back to Top Button

## 🚀 مراحل راه‌اندازی

### 1. نصب وابستگی‌های جدید

```bash
pip install -r requirements.txt
```

### 2. ایجاد Migration برای مدل‌های جدید

```bash
python manage.py makemigrations
```

این دستور migration برای مدل‌های جدید ایجاد می‌کند:
- `FAQ`
- `NewsletterSubscriber`

### 3. اعمال Migration

```bash
python manage.py migrate
```

### 4. ثبت مدل‌های جدید در Admin

مدل‌های جدید باید در `main/admin.py` ثبت شوند:

```python
from .models import FAQ, NewsletterSubscriber

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'active', 'created_at']
    list_filter = ['category', 'active']
    search_fields = ['question', 'answer']
    ordering = ['order', 'created_at']

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed', 'subscribed_at']
    list_filter = ['subscribed', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at', 'ip_address']
```

### 5. ایجاد فایل .env (اختیاری اما توصیه می‌شود)

برای production، یک فایل `.env` در root پروژه ایجاد کنید:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**نکته**: فایل `.env` را به `.gitignore` اضافه کنید!

### 6. جمع‌آوری فایل‌های استاتیک

```bash
python manage.py collectstatic
```

### 7. تست کردن

```bash
python manage.py runserver
```

سپس این صفحات را بررسی کنید:
- `/blog/` - صفحه بلاگ
- `/testimonials/` - نظرات مشتریان
- `/faq/` - سوالات متداول
- `/newsletter/subscribe/` - ثبت‌نام خبرنامه (از footer)

## 📝 نکات مهم

### امنیت
- در production حتماً `DEBUG = False` باشد
- `SECRET_KEY` را از environment variable بخوانید
- `ALLOWED_HOSTS` را تنظیم کنید

### Rate Limiting
- فرم تماس: حداکثر 5 درخواست در دقیقه
- فرم Quote: حداکثر 3 درخواست در دقیقه
- Newsletter: حداکثر 3 درخواست در دقیقه

### Newsletter
- فرم Newsletter در footer اضافه شده است
- می‌توانید از admin panel مشترکین را مدیریت کنید
- برای یکپارچه‌سازی با Mailchimp/SendGrid، باید کد اضافه کنید

## 🔧 مشکلات احتمالی

### اگر migration خطا داد:
```bash
python manage.py makemigrations main
python manage.py migrate main
```

### اگر static files لود نمی‌شوند:
```bash
python manage.py collectstatic --noinput
```

### اگر rate limiting کار نمی‌کند:
مطمئن شوید که `django-ratelimit` نصب شده است:
```bash
pip install django-ratelimit>=4.1.0
```

## ✅ چک‌لیست نهایی

- [ ] وابستگی‌ها نصب شده
- [ ] Migration ها اعمال شده
- [ ] مدل‌ها در admin ثبت شده
- [ ] فایل .env ایجاد شده (برای production)
- [ ] Static files جمع‌آوری شده
- [ ] صفحات جدید تست شده
- [ ] Rate limiting کار می‌کند
- [ ] Newsletter form کار می‌کند

## 📞 پشتیبانی

اگر مشکلی پیش آمد، لاگ‌ها را در `logs/django.log` بررسی کنید.

---

**تاریخ**: 2026-01-27
**نسخه**: 1.0
