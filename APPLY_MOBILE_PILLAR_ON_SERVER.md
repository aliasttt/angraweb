# تغییرات Pillar موبایل — برای اعمال روی سرور

## فایل‌های تغییر کرده

1. **`seo_pages/content/generator_tr.py`**
2. **`seo_pages/content/generator_en.py`**

---

## روش ۱: کپی مستقیم (ساده‌ترین)

از همین پروژه روی ویندوز، این دو فایل را روی سرور کپی کنید:

```bash
# از ویندوز (PowerShell) یا بعد از آپلود پروژه روی سرور:
scp "c:\Users\L E N O V O\Desktop\angraweb\seo_pages\content\generator_tr.py" user@SERVER:/path/to/angraweb/seo_pages/content/
scp "c:\Users\L E N O V O\Desktop\angraweb\seo_pages\content\generator_en.py" user@SERVER:/path/to/angraweb/seo_pages/content/
```

یا با rsync:

```bash
rsync -avz "c:/Users/L E N O V O/Desktop/angraweb/seo_pages/content/generator_tr.py" "c:/Users/L E N O V O/Desktop/angraweb/seo_pages/content/generator_en.py" user@SERVER:/path/to/angraweb/seo_pages/content/
```

بعد روی سرور اگر از Gunicorn/uWSGI استفاده می‌کنید سرویس را یک‌بار ریستارت کنید.

---

## روش ۲: فقط با Git

اگر روی سرور هم از همین ریپو استفاده می‌کنید:

1. همین‌جا commit کنید:
   ```bash
   git add seo_pages/content/generator_tr.py seo_pages/content/generator_en.py
   git commit -m "feat(seo): custom pillar TR/EN for mobile-app-development"
   git push
   ```
2. روی سرور:
   ```bash
   cd /path/to/angraweb
   git pull
   # سپس ریستارت اپ (systemctl restart gunicorn یا هر چی دارید)
   ```

---

## خلاصهٔ تغییرات

- **TR:** تابع `_mobile_app_pillar_tr` اضافه شده و در `generate_tr` برای `page_type == TYPE_PILLAR` و `service.key == "mobile-app-development"` صدا زده می‌شود. URL: `/tr/mobil-uygulama-gelistirme/`
- **EN:** تابع `_mobile_app_pillar_en` اضافه شده و در `generate_en` برای همان شرط. URL: `/en/mobile-app-development/`

بدنه و FAQ بدون کلمات قیمت‌گذاری (fiyat, maliyet, price, cost و ...) است.
