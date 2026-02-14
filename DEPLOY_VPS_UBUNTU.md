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
USE_POSTGRES=True
POSTGRES_DB=angraweb_db
POSTGRES_USER=angraweb_user
POSTGRES_PASSWORD=YOUR_DB_PASSWORD
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
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
Environment="PATH=/var/www/angraweb/venv/bin"
Environment="DEBUG=False"
Environment="SECRET_KEY=your-secret-key-here"
Environment="ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com"
Environment="USE_POSTGRES=True"
Environment="POSTGRES_DB=angraweb_db"
Environment="POSTGRES_USER=angraweb_user"
Environment="POSTGRES_PASSWORD=YOUR_DB_PASSWORD"
Environment="POSTGRES_HOST=localhost"
Environment="POSTGRES_PORT=5432"
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

## ۹) پیکربندی Nginx

```bash
nano /etc/nginx/sites-available/angraweb
```

محتوا (دامنه و مسیرها را عوض کنید):

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 50M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/angraweb/staticfiles/;
    }

    location /media/ {
        alias /var/www/angraweb/media/;
    }

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/var/www/angraweb/angraweb.sock;
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
