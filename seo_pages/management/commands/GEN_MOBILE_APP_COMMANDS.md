# دستورات generate_seo_content برای سرویس Mobile App Development
# استفاده: python manage.py generate_seo_content --force --service mobile-app-development ...

# ========== PILLAR (صفحهٔ اصلی سیلو) ==========
# TR: /tr/mobil-uygulama-gelistirme/
python manage.py generate_seo_content --force --service mobile-app-development --page-type pillar --language tr

# EN: /en/mobile-app-development/
python manage.py generate_seo_content --force --service mobile-app-development --page-type pillar --language en


# ========== CLUSTER — ترکی (TR) ==========
python manage.py generate_seo_content --force --service mobile-app-development --slug react-native --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug android --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug ios --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug ozel-mobil-uygulama --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug istanbul --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug mobil-uygulama-nedir --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug mobil-uygulama-nasil-yapilir --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug mobil-uygulama-freelancer --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug react-native-vs-native --language tr
python manage.py generate_seo_content --force --service mobile-app-development --slug android-vs-ios --language tr


# ========== CLUSTER — انگلیسی (EN) ==========
python manage.py generate_seo_content --force --service mobile-app-development --slug react-native-app-development --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug android-app-development --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug ios-app-development --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug custom-mobile-app-development --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug mobile-app-development-company --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug what-is-mobile-app-development --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug hire-mobile-app-developer --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug react-native-vs-native --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug cross-platform-vs-native --language en
python manage.py generate_seo_content --force --service mobile-app-development --slug mobile-app-development-cost --language en


# ========== یک‌جا همهٔ صفحات موبایل (هر دو زبان) ==========
# بدون --slug و بدون --page-type => همهٔ انواع صفحه (pillar, guide, pricing, quote, cluster)
python manage.py generate_seo_content --force --service mobile-app-development --language all
