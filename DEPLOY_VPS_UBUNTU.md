# راهنمای دیپلوی پروژه Angraweb روی VPS اوبونتو

این سند دستورات را **به ترتیب** برای آماده‌سازی و دیپلوی روی یک VPS اوبونتو (با Gunicorn، PostgreSQL، Nginx و SSL) توضیح می‌دهد.

---

## پیش‌نیاز

- یک VPS اوبونتو 22.04 (یا 20.04)
- دامنه‌ای که به IP سرور اشاره کند (برای SSL)
- دسترسی SSH به سرور

---

## ۱) ورود به سرور و به‌روزرسانی سیستم

```bash
ssh root@IP_SERVER
# یا: ssh ubuntu@IP_SERVER
```

```bash
apt update && apt upgrade -y
```

---

## ۲) نصب Python، PostgreSQL، Nginx و Certbot

```bash
apt install -y python3 python3-pip python3-venv python3-dev \
  postgresql postgresql-contrib libpq-dev \
  nginx certbot python3-certbot-nginx \
  git build-essential
```

---

## ۳) ساخت کاربر و دیتابیس PostgreSQL

```bash
sudo -u postgres psql
```

داخل `psql` این دستورات را **یکی‌یکی** بزنید (رمز قوی برای `YOUR_DB_PASSWORD` بگذارید):

```sql
CREATE USER angraweb_user WITH PASSWORD 'YOUR_DB_PASSWORD';
CREATE DATABASE angraweb_db OWNER angraweb_user;
ALTER ROLE angraweb_user SET client_encoding TO 'utf8';
ALTER ROLE angraweb_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE angraweb_user SET timezone TO 'Europe/Istanbul';
GRANT ALL PRIVILEGES ON DATABASE angraweb_db TO angraweb_user;
\q
```

---

## ۴) آپلود پروژه به سرور

**روی ویندوز (PowerShell یا CMD)** از همان پوشه پروژه:

```bash
scp -r "c:\Users\L E N O V O\Desktop\angraweb" root@IP_SERVER:/var/www/angraweb
```

یا با **rsync** (اگر نصب باشد):

```bash
rsync -avz --exclude "__pycache__" --exclude "*.pyc" --exclude "db.sqlite3" --exclude ".git" "c:\Users\L E N O V O\Desktop\angraweb" root@IP_SERVER:/var/www/angraweb
```

یا با **Git**: روی سرور:

```bash
mkdir -p /var/www && cd /var/www
git clone YOUR_REPO_URL angraweb
cd angraweb
```

اگر با SCP/rsync آپلود کردید، روی سرور اطمینان حاصل کنید پوشه `/var/www/angraweb` وجود دارد و فایل‌های پروژه داخل آن است.

---

## ۵) محیط مجازی Python و نصب وابستگی‌ها

روی سرور:

```bash
cd /var/www/angraweb
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ۶) فایل محیط (.env)

روی سرور در مسیر پروژه:

```bash
nano /var/www/angraweb/.env
```

این محتوا را بگذارید (مقادیر را با مقادیر واقعی عوض کنید):

```env
DEBUG=False
SECRET_KEY=یک-رشته-تصادفی-طولانی-و-امن-اینجا-بگذارید
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,IP_SERVER
CANONICAL_DOMAIN=https://yourdomain.com
STATIC_VERSION=1
USE_POSTGRES=True
POSTGRES_DB=angraweb_db
POSTGRES_USER=angraweb_user
POSTGRES_PASSWORD=YOUR_DB_PASSWORD
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
INSIGHTS_GSC_SITE_URL=sc-domain:angraweb.com
INSIGHTS_GSC_CREDENTIALS_JSON=/srv/angraweb/gsc.json
```

ذخیره: `Ctrl+O`, `Enter`, خروج: `Ctrl+X`.

**بارگذاری .env در Django:** فعلاً Django به‌صورت پیش‌فرض `.env` را نمی‌خواند. باید یا با `python-dotenv` بارگذاری شود یا متغیرها را در systemd قرار دهیم. در مرحله systemd متغیرها را مستقیم در فایل سرویس می‌گذاریم؛ اگر ترجیح می‌دهید از فایل `.env` استفاده کنید، این را نصب کنید:

```bash
source /var/www/angraweb/venv/bin/activate
pip install python-dotenv
```

و در **اول** فایل `angraweb_project/settings.py` (قبل از هر چیز) اضافه کنید:

```python
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')   # بعد از تعریف BASE_DIR
```

برای سادگی، در دستورالعمل زیر از **متغیرهای محیط در systemd** استفاده می‌کنیم و نیازی به ویرایش `settings.py` برای dotenv نیست؛ فقط همان مقادیر را در سرویس Gunicorn کپی می‌کنید.

---

## ۷) متغیرهای محیط برای اجرای دستی (تست)

برای تست قبل از systemd، یک‌بار این‌ها را در همان شل بزنید (مقادیر را عوض کنید):

```bash
cd /var/www/angraweb
source venv/bin/activate
export DEBUG=False
export SECRET_KEY="your-secret-key-here"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com,127.0.0.1"
export USE_POSTGRES=True
export POSTGRES_DB=angraweb_db
export POSTGRES_USER=angraweb_user
export POSTGRES_PASSWORD="YOUR_DB_PASSWORD"
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

سپس:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py check
```

اگر خطایی نبود، با Gunicorn تست کنید:

```bash
gunicorn --bind 0.0.0.0:8000 angraweb_project.wsgi:application
```

در مرورگر بزنید: `http://IP_SERVER:8000`. اگر سایت باز شد، `Ctrl+C` بزنید و مرحله بعد را انجام دهید.

---

## ۸) سرویس Systemd برای Gunicorn

```bash
nano /etc/systemd/system/angraweb.service
```

محتوا (مسیرها و مقادیر را با خود سرور تطبیق دهید):

```ini
[Unit]
Description=Angraweb Gunicorn
After=network.target postgresql.service

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/angraweb
EnvironmentFile=-/etc/angraweb/angraweb.env
Environment="PATH=/var/www/angraweb/venv/bin"
Environment="DEBUG=False"
Environment="SECRET_KEY=your-secret-key-here"
Environment="ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com"
Environment="CANONICAL_DOMAIN=https://yourdomain.com"
Environment="USE_POSTGRES=True"
Environment="POSTGRES_DB=angraweb_db"
Environment="POSTGRES_USER=angraweb_user"
Environment="POSTGRES_PASSWORD=YOUR_DB_PASSWORD"
Environment="POSTGRES_HOST=localhost"
Environment="POSTGRES_PORT=5432"
Environment="INSIGHTS_GSC_SITE_URL=sc-domain:angraweb.com"
Environment="INSIGHTS_GSC_CREDENTIALS_JSON=/srv/angraweb/gsc.json"
ExecStart=/var/www/angraweb/venv/bin/gunicorn --workers 3 --bind unix:/var/www/angraweb/angraweb.sock angraweb_project.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

فعال و اجرا:

```bash
systemctl daemon-reload
systemctl enable angraweb
systemctl start angraweb
systemctl status angraweb
```

---

## قدم ۴ – ست کردن GSC (Google Search Console) روی سرور

برای داشتن دادهٔ واقعی SEO در داشبورد Insights باید کلید سرویس (Service Account) گوگل را روی سرور ست کنی.

### ۱) آپلود فایل JSON روی سرور

فایل JSON که از Google Cloud Console گرفتی (مثلاً `gen-lang-client-0574560023-d10a164b0ddd.json`) را روی سرور بگذار، مثلاً:

```bash
# روی ویندوز (PowerShell) از پوشهٔ Downloads:
scp "gen-lang-client-0574560023-d10a164b0ddd.json" root@IP_SERVER:/srv/angraweb/gsc.json
```

یا با نام دیگر؛ فقط مسیر را بعداً در env استفاده کن.

روی سرور مطمئن شو فایل خوانا است و دسترسی امن است:

```bash
chmod 600 /srv/angraweb/gsc.json
```

### ۲) تنظیم متغیرهای محیط

**اگر از Domain property استفاده می‌کنی** (مثل `angraweb.com` بدون پیشوند URL):

در `.env` یا در سرویس systemd این دو خط را اضافه کن:

```env
INSIGHTS_GSC_SITE_URL=sc-domain:angraweb.com
INSIGHTS_GSC_CREDENTIALS_JSON=/srv/angraweb/gsc.json
```

**اگر از URL-prefix property استفاده می‌کنی** (مثل `https://angraweb.com/`):

```env
INSIGHTS_GSC_SITE_URL=https://angraweb.com/
INSIGHTS_GSC_CREDENTIALS_JSON=/srv/angraweb/gsc.json
```

در **systemd** (فایل `/etc/systemd/system/angraweb.service`) همین دو خط را در بخش `[Service]` داخل `Environment=` اضافه کن (در همین سند قبلاً به نمونه systemd اضافه شده است).

بعد از ذخیره:

```bash
systemctl daemon-reload
systemctl restart angraweb
```

### ۳) تست و اجرای سنک

روی سرور:

```bash
cd /srv/angraweb
source venv/bin/activate
export INSIGHTS_GSC_SITE_URL=sc-domain:angraweb.com
export INSIGHTS_GSC_CREDENTIALS_JSON=/srv/angraweb/gsc.json
python manage.py insights_sync_gsc --days 28
```

اگر خطایی نبود، دادهٔ GSC در ادمین و داشبورد `/admin/insights/` نمایش داده می‌شود. می‌توانی این دستور را با cron روزانه اجرا کنی.

---

## ۹) پیکربندی Nginx

```bash
nano /etc/nginx/sites-available/angraweb
```

محتوا (دامنه و مسیرها را عوض کنید):

```nginx
# مهم: مسیرها باید همان مسیری باشد که اسکریپت دپلوی استفاده می‌کند (مثلاً /srv/angraweb).
# اگر پروژه در /srv/angraweb است، حتماً همین مسیر را اینجا هم بگذارید وگرنه بعد از هر دپلوی استاتیک قدیمی سرو می‌شود.
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 50M;

    location = /favicon.ico { access_log off; log_not_found off; }

    # استاتیک: بدون کش طولانی تا بعد از هر دپلوی CSS/JS جدید لود شود (جلوگیری از استایل/انیمیشن قدیمی)
    location /static/ {
        alias /srv/angraweb/staticfiles/;
        add_header Cache-Control "public, max-age=0, must-revalidate";
    }

    location /media/ {
        alias /srv/angraweb/media/;
    }

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/srv/angraweb/angraweb.sock;
    }
}
```

فعال‌سازی سایت و تست Nginx:

```bash
ln -s /etc/nginx/sites-available/angraweb /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

الان با `http://yourdomain.com` باید سایت بدون SSL بالا بیاید.

---

## ۱۰) نصب SSL با Certbot (Let's Encrypt)

```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

ایمیل را وارد کنید و قوانین را بپذیرید. بعد از اتمام، Nginx به‌صورت خودکار با HTTPS پیکربندی می‌شود.

تجدید خودکار:

```bash
certbot renew --dry-run
```

---

## ۱۱) فایروال (اختیاری ولی توصیه‌شده)

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
ufw status
```

---

## ۱۲) دستورات مفید بعد از دیپلوی

- ریستارت اپ:

```bash
systemctl restart angraweb
```

- مشاهده لاگ Gunicorn:

```bash
journalctl -u angraweb -f
```

- به‌روزرسانی کد و استاتیک و مایگریشن:

```bash
cd /var/www/angraweb
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
systemctl restart angraweb
```

---

## ۱۳) همگام‌سازی همهٔ تغییرات لوکال با سرور

هر وقت روی لوکال چیز جدیدی اضافه کردید (صفحات، پکیج‌ها، پروژه‌ها، قالب، استاتیک و…) باید دو کار انجام شود: **به‌روزرسانی کد روی سرور** و در صورت نیاز **به‌روزرسانی داده (دیتابیس)**.

### الف) روی ویندوز (لوکال) — قبل از هر چیز

۱. همهٔ تغییرات را کامیت و پوش کنید تا روی سرور بتوانید `git pull` بزنید:

```powershell
cd "c:\Users\L E N O V O\Desktop\angraweb"
git add .
git status
# اگر فقط db.sqlite3 تغییر کرده، آن را اضافه نکنید (یا در .gitignore باشد)
git restore --staged db.sqlite3
git commit -m "توضیح تغییرات"
git push origin main
```

اگر از **Git روی سرور** استفاده نمی‌کنید و با **SCP یا rsync** کد را کپی می‌کنید، همین پوشه را دوباره به سرور بفرستید (مطابق بخش ۴).

### ب) روی سرور — به‌روزرسانی کد و اپ

**اگر روی سرور از Git استفاده می‌کنید:**

```bash
cd /var/www/angraweb
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart angraweb
```

**اگر با SCP/rsync کد می‌فرستید:** بعد از کپی کردن فایل‌ها روی سرور همان سه خط آخر را اجرا کنید (بدون `git pull`):

```bash
cd /var/www/angraweb
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart angraweb
```

### ج) اگر روی سرور پکیج‌ها یا پروژه‌ها خالی است (صفحه پکیج/پروژه خالی است)

محتوای صفحه «پکیج‌ها» و «پروژه‌ها» از **دیتابیس** می‌آید. اگر روی سرور تازه نصب کرده‌اید یا دیتابیس خالی است، باید داده را از لوکال به سرور منتقل کنید.

**۱) روی ویندوز (لوکال)** — خروجی گرفتن از دیتابیس لوکال (فقط اپ `main`):

اگر خطای encoding (مثل `charmap can't encode`) گرفتید، از این استفاده کنید:

```powershell
cd "c:\Users\L E N O V O\Desktop\angraweb"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python manage.py dumpdata main.Service main.Package main.PackageFeature main.Project main.ProjectVideo main.Testimonial --indent 2 | Out-File -FilePath main_data.json -Encoding utf8
```

در غیر این صورت:

```powershell
cd "c:\Users\L E N O V O\Desktop\angraweb"
python manage.py dumpdata main.Service main.Package main.PackageFeature main.Project main.ProjectVideo main.Testimonial --indent 2 -o main_data.json
```

فایل `main_data.json` در پوشه پروژه ساخته می‌شود. این فایل را با SCP یا هر روش دیگر به سرور ببرید، مثلاً در `/var/www/angraweb/`.

**۲) روی سرور** — وارد کردن همان داده در دیتابیس سرور:

```bash
cd /var/www/angraweb
source venv/bin/activate
python manage.py loaddata main_data.json
systemctl restart angraweb
```

اگر خطای تکراری (duplicate key) گرفتید، یعنی آن رکوردها از قبل روی سرور وجود دارند؛ یا از ادمین سرور محتوا را ویرایش کنید یا فقط مدل‌هایی را که خالی هستند در `dumpdata` بگذارید.

**راه دیگر:** از **پنل ادمین Django روی سرور** (`https://yourdomain.com/admin/`) با یک سوپریوزر وارد شوید و پکیج‌ها و پروژه‌ها را دستی اضافه کنید.

---

## خلاصه ترتیب دستورات (چک‌لیست)

| مرحله | کار |
|-------|-----|
| 1 | `apt update && apt upgrade -y` |
| 2 | نصب Python, PostgreSQL, Nginx, Certbot |
| 3 | ساخت کاربر و دیتابیس در PostgreSQL |
| 4 | آپلود پروژه به `/var/www/angraweb` |
| 5 | ساخت venv و `pip install -r requirements.txt` |
| 6 | ساخت `.env` (یا آماده‌سازی مقادیر برای systemd) |
| 7 | `collectstatic`, `migrate`, تست با `gunicorn` |
| 8 | ساخت و فعال کردن سرویس `angraweb.service` |
| 9 | پیکربندی Nginx و `nginx -t` و `reload` |
| 10 | `certbot --nginx -d yourdomain.com -d www.yourdomain.com` |
| 11 | (اختیاری) `ufw` |

با انجام این مراحل، پروژه با Gunicorn، PostgreSQL، Nginx و SSL روی VPS اوبونتو آماده سرویس‌دهی است.





sudo -u angraweb bash -lc "
cd /srv/angraweb || exit 1

# Git: fix safe directory + pull latest
git config --global --add safe.directory /srv/angraweb
# If unmerged files (conflict): abort merge and reset to remote so pull can run
git merge --abort 2>/dev/null || true
git fetch origin
git reset --hard origin/main
git pull --ff-only || exit 1

# Load env + activate venv
set -a
source /etc/angraweb/angraweb.env
set +a
source /srv/angraweb/venv/bin/activate

# Django tasks
python manage.py migrate --noinput || exit 1
python manage.py collectstatic --noinput || exit 1


"

# به‌روزرسانی STATIC_VERSION تا بعد از دپلوی کش مرورگر/Nginx فایل‌های جدید CSS/JS را بگیرد
ENVFILE=/etc/angraweb/angraweb.env
if [ -f "$ENVFILE" ]; then
  NEW_VER=$(date +%s)
  if grep -q '^STATIC_VERSION=' "$ENVFILE" 2>/dev/null; then
    sudo sed -i "s/^STATIC_VERSION=.*/STATIC_VERSION=$NEW_VER/" "$ENVFILE"
  else
    echo "STATIC_VERSION=$NEW_VER" | sudo tee -a "$ENVFILE" >/dev/null
  fi
fi

# اگر Nginx از مسیر دیگری استاتیک سرو می‌کند (مثلاً /var/www/angraweb)، بعد از collectstatic کپی کن
# وگرنه همین که Nginx همان مسیر پروژه را ببیند (مثلاً /srv/angraweb/staticfiles/) کافی است.
PROJECT_ROOT=/srv/angraweb
NGINX_STATIC=/var/www/angraweb/staticfiles
if [ -d "$NGINX_STATIC" ] && [ "$(readlink -f "$PROJECT_ROOT/staticfiles" 2>/dev/null)" != "$(readlink -f "$NGINX_STATIC" 2>/dev/null)" ]; then
  echo "Syncing staticfiles to Nginx path..."
  sudo rsync -a --delete "$PROJECT_ROOT/staticfiles/" "$NGINX_STATIC/"
fi

# Restart services
sudo systemctl restart angraweb
sudo systemctl restart nginx

# Quick health check
curl -I https://angraweb.com | head -n 20
```

---

## چرا بعد از هر دپلوی استایل/انیمیشن خراب می‌شود؟

**علت اصلی:** مسیر پروژه در اسکریپت دپلوی با مسیر استاتیک در Nginx یکی نیست. اسکریپت در `/srv/angraweb` اجرا می‌شود و `collectstatic` فایل‌های جدید را در `/srv/angraweb/staticfiles/` می‌ریزد؛ اگر در Nginx از `alias /var/www/angraweb/staticfiles/` استفاده شده باشد، Nginx همان فایل‌های **قدیمی** را سرو می‌کند و هر بار دپلوی انگار استاتیک به‌روز نمی‌شود.

**راه‌حل (یکی از این دو):**
1. **توصیه:** در Nginx مسیر استاتیک و سوکت را به همان مسیر پروژه تغییر بده: `alias /srv/angraweb/staticfiles/` و `proxy_pass ... unix:/srv/angraweb/angraweb.sock` (نمونهٔ به‌روز در همین سند هست).
2. یا اسکریپت دپلوی را همان‌طور که الان هست نگه دار؛ بلوک **rsync** قبل از restart استاتیک را از `/srv/angraweb/staticfiles/` به `/var/www/angraweb/staticfiles/` کپی می‌کند تا اگر Nginx هنوز از مسیر دوم استفاده می‌کند، فایل‌های جدید آنجا هم بروند.

---

## جلوگیری از کش قدیمی CSS/JS بعد از دپلوی

اگر بعد از هر دپلوی استایل‌ها یا انیمیشن‌های صفحهٔ هوم درست لود نمی‌شوند (یا CSS/JS اورراید می‌شود)، علت می‌تواند **مسیر Nginx** (بالا) یا **کش مرورگر/Nginx** باشد.

**راه‌حل:** پروژه از متغیر محیطی `STATIC_VERSION` استفاده می‌کند. با هر بار عوض شدن این مقدار، آدرس فایل‌های CSS/JS در HTML عوض می‌شود (`?v=...`) و مرورگر فایل جدید را می‌گیرد.

- در **فایل env** (مثلاً `/etc/angraweb/angraweb.env`) یک خط اضافه کنید:
  ```env
  STATIC_VERSION=1
  ```
- در اسکریپت دپلوی (بالا) قبل از `systemctl restart angraweb` مقدار `STATIC_VERSION` با تایم‌استامپ به‌روز می‌شود تا هر دپلوی نسخهٔ جدید استاتیک اعمال شود.
- اگر از systemd استفاده می‌کنید، مطمئن شوید سرویس با `EnvironmentFile=/etc/angraweb/angraweb.env` این فایل را می‌خواند تا `STATIC_VERSION` به اپ پاس شود.

**اگر هنوز استایل/انیمیشن قدیمی لود می‌شود (یا Bootstrap اورراید می‌کند):**

1. **Nginx:** در `location /static/` حتماً این هدر را داشته باشید تا کش طولانی نشود:
   ```nginx
   add_header Cache-Control "public, max-age=0, must-revalidate";
   ```
   بعد: `sudo nginx -t && sudo systemctl reload nginx`

2. **مسیر استاتیک:** در همان کانفیگ Nginx باید `alias` به همان پوشه‌ای باشد که `collectstatic` پر می‌کند، مثلاً:
   `alias /srv/angraweb/staticfiles/;`

3. **بررسی روی سرور:** مطمئن شوی فایل واقعاً به‌روز است:
   ```bash
   head -n 25 /srv/angraweb/staticfiles/css/style.css
   ```
   باید خطوطی مثل `hero-section__` یا `whatsapp-cta` در فایل باشد؛ اگر نیست، دوباره از همان پوشهٔ پروژه `collectstatic` بزن و سرویس را ریستارت کن.

4. **مرورگر:** یک بار Hard Refresh (Ctrl+Shift+R یا Cmd+Shift+R) یا کش مرورگر را برای دامنه پاک کن.

**نکته (Lighthouse/PageSpeed):** برای بهبود امتیاز عملکرد، انیمیشن‌های صفحهٔ هوم حذف نشوند. در قالب، `style.css` همیشه **آخر** در `<head>` لود می‌شود و کلاس `animations-on` روی `<body>` قرار دارد تا استایل و انیمیشن‌ها (هیرو، نوار سرویس‌ها، پس‌زمینه) درست کار کنند.

---

## چاپ لاگ برای دیباگ خطای ۵۰۰ (کپی در ترمینال VPS)

این بلوک را روی سرور اجرا کنید و **خروجی کامل** را کپی کرده اینجا بفرستید تا علت خطا مشخص شود:

```bash
echo "========== 1) آخرین لاگ سرویس angraweb (journalctl) =========="
sudo journalctl -u angraweb -n 200 --no-pager

echo ""
echo "========== 2) فایل لاگ Django (در صورت وجود) =========="
for dir in /srv/angraweb /var/www/angraweb; do
  if [ -f "$dir/logs/django.log" ]; then
    echo "--- $dir/logs/django.log (آخرین 150 خط) ---"
    sudo tail -n 150 "$dir/logs/django.log"
    break
  fi
done
```












141.98.51.168


























You are an SEO content editor and web content designer.

Improve and expand the following blog article.

Do NOT completely rewrite the article.
Keep the main ideas but improve the structure, readability, design and SEO.

GOALS

• Expand the article to around 1200–1400 words  
• Improve clarity and readability  
• Improve SEO structure  
• Improve user experience while reading  
• Keep the article natural and informative  

SEO IMPROVEMENTS

• Add proper heading hierarchy (H1, H2, H3)  
• Improve keyword usage naturally  
• Add internal links to relevant pillar and cluster pages  
• Make sure internal links are contextually relevant to the section topic  

Example internal linking strategy:
If the section talks about corporate websites → link to /kurumsal-web-sitesi  
If the section talks about web design → link to /profesyonel-web-tasarim  
If the section talks about SEO → link to /seo-consulting  
If the section talks about hosting → link to /vps-hosting  
If the section talks about backend or development → link to /django-web-gelistirme  

CONTENT STRUCTURE

Use correct semantic structure:

H1 → Article title  
H2 → Main sections  
H3 → Subsections  

Include these sections if missing:

• Dark Mode Design  
• 3D Web Elements  
• Bento Grid Layout  
• AI Driven Web Experience  

READABILITY IMPROVEMENTS

Do not produce a wall of text.

Improve reading experience by using:

• short paragraphs  
• bullet lists  
• highlighted key points  
• section summaries  

Add visually structured sections such as:

• Key benefits lists  
• Tips boxes  
• Important notes  

Make the article comfortable and engaging for readers.

INTERNAL LINKS

Use these internal links naturally where relevant:

/kurumsal-web-sitesi  
/profesyonel-web-tasarim  
/seo-consulting  
/vps-hosting  
/django-web-gelistirme  

INTRODUCTION

Improve the introduction to 150–200 words.

The introduction should:

• explain the topic clearly  
• include important keywords  
• attract reader attention  

CONCLUSION

Improve the conclusion and add a strong call-to-action encouraging readers to explore services or contact the company.

FAQ SECTION

Add an SEO optimized FAQ section with 4 questions.

Use proper structure:

H2 → Sıkça Sorulan Sorular  
H3 → Question  

LANGUAGE

Keep the article in Turkish language.

OUTPUT FORMAT

Return the article as clean structured HTML content ready for publishing.

Use structured sections such as:

<section>
<div>
<ul>
<strong>
<h1>
<h2>
<h3>

Make sure the article is visually structured and not just plain text.