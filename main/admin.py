from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Service, Package, PackageFeature, Project, ProjectVideo,
    Certificate, ContactMessage, QuoteRequest, BlogPost,
    Testimonial, SiteSetting
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'featured', 'order', 'active', 'created_at']
    list_filter = ['service_type', 'featured', 'active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['featured', 'order', 'active']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'slug', 'service_type')
        }),
        ('توضیحات', {
            'fields': ('description', 'description_en', 'description_fa', 'description_ar')
        }),
        ('رسانه', {
            'fields': ('icon', 'image')
        }),
        ('تنظیمات', {
            'fields': ('featured', 'order', 'active')
        }),
    )


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 3
    fields = ['title', 'title_en', 'title_fa', 'title_ar', 'included', 'order']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'package_type', 'price', 'currency', 'featured', 'popular', 'order', 'active']
    list_filter = ['package_type', 'featured', 'popular', 'active']
    search_fields = ['title', 'description']
    list_editable = ['featured', 'popular', 'order', 'active']
    inlines = [PackageFeatureInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'package_type')
        }),
        ('قیمت', {
            'fields': ('price', 'currency', 'custom_price_text')
        }),
        ('توضیحات', {
            'fields': ('description', 'description_en', 'description_fa', 'description_ar')
        }),
        ('تنظیمات', {
            'fields': ('featured', 'popular', 'order', 'active')
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'domain', 'featured', 'order', 'active', 'created_at']
    list_filter = ['project_type', 'featured', 'active', 'created_at']
    search_fields = ['title', 'description', 'domain']
    list_editable = ['featured', 'order', 'active']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'slug', 'project_type')
        }),
        ('توضیحات', {
            'fields': ('description', 'description_en', 'description_fa', 'description_ar')
        }),
        ('لینک و تصاویر', {
            'fields': ('url', 'domain', 'image', 'thumbnail')
        }),
        ('تکنولوژی‌ها', {
            'fields': ('technologies',)
        }),
        ('تنظیمات', {
            'fields': ('featured', 'order', 'active')
        }),
    )


@admin.register(ProjectVideo)
class ProjectVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'order', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'active']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'order', 'active']
    list_filter = ['active', 'issue_date']
    search_fields = ['title', 'issuer']
    list_editable = ['order', 'active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_type', 'status', 'created_at']
    list_filter = ['status', 'service_type', 'created_at']
    search_fields = ['name', 'email', 'company', 'description']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات تماس', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('جزئیات پروژه', {
            'fields': ('service_type', 'package_type', 'description', 'budget', 'deadline')
        }),
        ('وضعیت', {
            'fields': ('status', 'admin_notes')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'featured', 'published', 'views', 'created_at']
    list_filter = ['featured', 'published', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['featured', 'published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'slug', 'author')
        }),
        ('خلاصه', {
            'fields': ('excerpt', 'excerpt_en', 'excerpt_fa', 'excerpt_ar')
        }),
        ('محتوا', {
            'fields': ('content', 'content_en', 'content_fa', 'content_ar')
        }),
        ('رسانه', {
            'fields': ('image',)
        }),
        ('تنظیمات', {
            'fields': ('featured', 'published', 'published_at', 'views')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'featured', 'order', 'active']
    list_filter = ['rating', 'featured', 'active']
    search_fields = ['name', 'company', 'content']
    list_editable = ['featured', 'order', 'active']


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'description']
    search_fields = ['key', 'description']
