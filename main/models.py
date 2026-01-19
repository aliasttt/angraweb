from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Service(models.Model):
    """مدل برای خدمات"""
    SERVICE_TYPES = [
        ('web_design', 'طراحی وبسایت'),
        ('mobile_app', 'طراحی اپلیکیشن موبایل'),
        ('ecommerce', 'فروشگاه اینترنتی'),
        ('seo', 'سئو و بهینه‌سازی'),
        ('hosting', 'هاستینگ و دامنه'),
        ('ui_ux', 'طراحی UI/UX'),
        ('custom', 'سفارشی'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='اسلاگ')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, verbose_name='نوع خدمت')
    
    description = models.TextField(verbose_name='توضیحات')
    description_en = models.TextField(blank=True, verbose_name='توضیحات انگلیسی')
    description_fa = models.TextField(blank=True, verbose_name='توضیحات فارسی')
    description_ar = models.TextField(blank=True, verbose_name='توضیحات عربی')
    
    icon = models.CharField(max_length=100, default='fas fa-code', verbose_name='آیکون')
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name='تصویر')
    
    featured = models.BooleanField(default=False, verbose_name='ویژه')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class Package(models.Model):
    """مدل برای پکیج‌ها"""
    PACKAGE_TYPES = [
        ('basic', 'پکیج پایه'),
        ('commercial', 'پکیج تجاری'),
        ('professional', 'پکیج حرفه‌ای'),
        ('custom', 'پکیج کاستوم'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    package_type = models.CharField(max_length=50, choices=PACKAGE_TYPES, verbose_name='نوع پکیج')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    currency = models.CharField(max_length=10, default='TL', verbose_name='واحد پول')
    custom_price_text = models.CharField(max_length=200, blank=True, verbose_name='متن قیمت سفارشی')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    description_en = models.TextField(blank=True, verbose_name='توضیحات انگلیسی')
    description_fa = models.TextField(blank=True, verbose_name='توضیحات فارسی')
    description_ar = models.TextField(blank=True, verbose_name='توضیحات عربی')
    
    featured = models.BooleanField(default=False, verbose_name='ویژه')
    popular = models.BooleanField(default=False, verbose_name='محبوب')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'پکیج'
        verbose_name_plural = 'پکیج‌ها'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title


class PackageFeature(models.Model):
    """ویژگی‌های پکیج"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='features', verbose_name='پکیج')
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    included = models.BooleanField(default=True, verbose_name='شامل شده')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    
    class Meta:
        verbose_name = 'ویژگی پکیج'
        verbose_name_plural = 'ویژگی‌های پکیج'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.package.title} - {self.title}"


class Project(models.Model):
    """مدل برای پروژه‌ها"""
    PROJECT_TYPES = [
        ('web', 'وبسایت'),
        ('mobile', 'اپلیکیشن موبایل'),
        ('ecommerce', 'فروشگاه اینترنتی'),
        ('platform', 'پلتفرم'),
        ('other', 'سایر'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='اسلاگ')
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES, verbose_name='نوع پروژه')
    
    description = models.TextField(verbose_name='توضیحات')
    description_en = models.TextField(blank=True, verbose_name='توضیحات انگلیسی')
    description_fa = models.TextField(blank=True, verbose_name='توضیحات فارسی')
    description_ar = models.TextField(blank=True, verbose_name='توضیحات عربی')
    
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='تصویر')
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True, null=True, verbose_name='تصویر کوچک')
    
    url = models.URLField(blank=True, verbose_name='لینک پروژه')
    domain = models.CharField(max_length=200, blank=True, verbose_name='دامنه')
    
    technologies = models.CharField(max_length=500, blank=True, verbose_name='تکنولوژی‌ها (جدا شده با کاما)')
    
    featured = models.BooleanField(default=False, verbose_name='ویژه')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_technologies_list(self):
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []


class ProjectVideo(models.Model):
    """ویدیوهای پروژه"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos', blank=True, null=True, verbose_name='پروژه')
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    video_file = models.FileField(upload_to='videos/', verbose_name='فایل ویدیو')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True, verbose_name='تصویر کوچک')
    
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'ویدیو پروژه'
        verbose_name_plural = 'ویدیوهای پروژه'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title


class Certificate(models.Model):
    """مدل برای گواهینامه‌ها"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    issuer = models.CharField(max_length=200, blank=True, verbose_name='صادرکننده')
    
    image = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name='تصویر')
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True, verbose_name='فایل PDF')
    
    issue_date = models.DateField(blank=True, null=True, verbose_name='تاریخ صدور')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='تاریخ انقضا')
    
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'گواهینامه'
        verbose_name_plural = 'گواهینامه‌ها'
        ordering = ['order', '-issue_date']
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """مدل برای پیام‌های تماس"""
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('read', 'خوانده شده'),
        ('replied', 'پاسخ داده شده'),
        ('archived', 'آرشیو شده'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='وضعیت')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='آدرس IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class QuoteRequest(models.Model):
    """درخواست قیمت"""
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('reviewed', 'بررسی شده'),
        ('quoted', 'قیمت داده شده'),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    company = models.CharField(max_length=200, blank=True, verbose_name='شرکت')
    
    service_type = models.CharField(max_length=100, verbose_name='نوع خدمت')
    package_type = models.CharField(max_length=100, blank=True, verbose_name='نوع پکیج')
    
    description = models.TextField(verbose_name='توضیحات پروژه')
    budget = models.CharField(max_length=100, blank=True, verbose_name='بودجه')
    deadline = models.CharField(max_length=100, blank=True, verbose_name='مهلت')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='وضعیت')
    admin_notes = models.TextField(blank=True, verbose_name='یادداشت ادمین')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'درخواست قیمت'
        verbose_name_plural = 'درخواست‌های قیمت'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.service_type}"


class BlogPost(models.Model):
    """پست‌های وبلاگ"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='عنوان انگلیسی')
    title_fa = models.CharField(max_length=200, blank=True, verbose_name='عنوان فارسی')
    title_ar = models.CharField(max_length=200, blank=True, verbose_name='عنوان عربی')
    
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='اسلاگ')
    
    excerpt = models.TextField(max_length=500, verbose_name='خلاصه')
    excerpt_en = models.TextField(max_length=500, blank=True, verbose_name='خلاصه انگلیسی')
    excerpt_fa = models.TextField(max_length=500, blank=True, verbose_name='خلاصه فارسی')
    excerpt_ar = models.TextField(max_length=500, blank=True, verbose_name='خلاصه عربی')
    
    content = models.TextField(verbose_name='محتوا')
    content_en = models.TextField(blank=True, verbose_name='محتوا انگلیسی')
    content_fa = models.TextField(blank=True, verbose_name='محتوا فارسی')
    content_ar = models.TextField(blank=True, verbose_name='محتوا عربی')
    
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='تصویر')
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='نویسنده')
    
    featured = models.BooleanField(default=False, verbose_name='ویژه')
    published = models.BooleanField(default=False, verbose_name='منتشر شده')
    
    views = models.IntegerField(default=0, verbose_name='بازدیدها')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')
    
    class Meta:
        verbose_name = 'پست وبلاگ'
        verbose_name_plural = 'پست‌های وبلاگ'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class Testimonial(models.Model):
    """نظرات مشتریان"""
    name = models.CharField(max_length=200, verbose_name='نام')
    company = models.CharField(max_length=200, blank=True, verbose_name='شرکت')
    position = models.CharField(max_length=200, blank=True, verbose_name='سمت')
    
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name='تصویر')
    
    content = models.TextField(verbose_name='متن نظر')
    content_en = models.TextField(blank=True, verbose_name='متن نظر انگلیسی')
    content_fa = models.TextField(blank=True, verbose_name='متن نظر فارسی')
    content_ar = models.TextField(blank=True, verbose_name='متن نظر عربی')
    
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name='امتیاز')
    
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پروژه')
    
    featured = models.BooleanField(default=False, verbose_name='ویژه')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'نظر مشتری'
        verbose_name_plural = 'نظرات مشتریان'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} ستاره"


class SiteSetting(models.Model):
    """تنظیمات سایت"""
    key = models.CharField(max_length=100, unique=True, verbose_name='کلید')
    value = models.TextField(verbose_name='مقدار')
    value_en = models.TextField(blank=True, verbose_name='مقدار انگلیسی')
    value_fa = models.TextField(blank=True, verbose_name='مقدار فارسی')
    value_ar = models.TextField(blank=True, verbose_name='مقدار عربی')
    
    description = models.CharField(max_length=500, blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'
    
    def __str__(self):
        return self.key
