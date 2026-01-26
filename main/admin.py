from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Service, Package, PackageFeature, Project, ProjectVideo,
    Certificate, ContactMessage, QuoteRequest, BlogPost,
    Testimonial, SiteSetting, TeamMember, UserProfile, FAQ, NewsletterSubscriber,
    ProcessStep, CaseStudy, TimelineEvent, Skill
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


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'years_experience', 'order', 'active']
    list_filter = ['role', 'active']
    search_fields = ['full_name', 'headline', 'bio', 'skills']
    list_editable = ['order', 'active']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username', 'phone']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'active', 'created_at']
    list_filter = ['category', 'active', 'created_at']
    search_fields = ['question', 'answer', 'question_en', 'question_fa', 'question_ar']
    list_editable = ['order', 'active']
    fieldsets = (
        ('سوال', {
            'fields': ('question', 'question_en', 'question_fa', 'question_ar')
        }),
        ('پاسخ', {
            'fields': ('answer', 'answer_en', 'answer_fa', 'answer_ar')
        }),
        ('تنظیمات', {
            'fields': ('category', 'order', 'active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed', 'subscribed_at']
    list_filter = ['subscribed', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at', 'ip_address']
    list_editable = ['subscribed']
    fieldsets = (
        ('اطلاعات', {
            'fields': ('email', 'name')
        }),
        ('وضعیت', {
            'fields': ('subscribed',)
        }),
        ('اطلاعات سیستم', {
            'fields': ('ip_address', 'subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title', 'duration', 'order', 'active']
    list_filter = ['active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'active']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'step_number', 'icon')
        }),
        ('توضیحات', {
            'fields': ('description', 'description_en', 'description_fa', 'description_ar')
        }),
        ('تنظیمات', {
            'fields': ('duration', 'order', 'active')
        }),
    )


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'client_industry', 'featured', 'order', 'active']
    list_filter = ['featured', 'active', 'client_industry', 'created_at']
    search_fields = ['title', 'client_name', 'challenge', 'solution']
    list_editable = ['featured', 'order', 'active']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'slug')
        }),
        ('اطلاعات مشتری', {
            'fields': ('client_name', 'client_industry')
        }),
        ('محتوا', {
            'fields': ('challenge', 'challenge_en', 'challenge_fa', 'challenge_ar',
                      'solution', 'solution_en', 'solution_fa', 'solution_ar',
                      'results', 'results_en', 'results_fa', 'results_ar')
        }),
        ('رسانه و لینک', {
            'fields': ('image_before', 'image_after', 'project_url')
        }),
        ('آمار و تکنولوژی', {
            'fields': ('metrics', 'technologies', 'project')
        }),
        ('تنظیمات', {
            'fields': ('featured', 'order', 'active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type', 'order', 'active']
    list_filter = ['event_type', 'active', 'date']
    search_fields = ['title', 'description']
    list_editable = ['order', 'active']
    date_hierarchy = 'date'
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'title_en', 'title_fa', 'title_ar', 'date', 'icon', 'event_type')
        }),
        ('توضیحات', {
            'fields': ('description', 'description_en', 'description_fa', 'description_ar')
        }),
        ('تنظیمات', {
            'fields': ('order', 'active')
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage', 'order', 'active']
    list_filter = ['category', 'active']
    search_fields = ['name']
    list_editable = ['percentage', 'order', 'active']
    fieldsets = (
        ('اطلاعات', {
            'fields': ('name', 'name_en', 'name_fa', 'name_ar', 'icon', 'category')
        }),
        ('تنظیمات', {
            'fields': ('percentage', 'order', 'active')
        }),
    )
