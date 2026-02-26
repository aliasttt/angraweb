from django.contrib import admin
from .models import (
    GSCQueryPageStat,
    GSCPageStat,
    SerpSnapshot,
    MetaAuditResult,
    InsightSession,
    InsightEvent,
    SEOHealthSnapshot,
    InsightAlert,
)


@admin.register(GSCQueryPageStat)
class GSCQueryPageStatAdmin(admin.ModelAdmin):
    list_display = ['date', 'query_short', 'page_short', 'clicks', 'impressions', 'ctr', 'position']
    list_filter = ['date']
    search_fields = ['query', 'page']
    date_hierarchy = 'date'

    def query_short(self, obj):
        return (obj.query or '')[:50]
    query_short.short_description = 'Query'

    def page_short(self, obj):
        return (obj.page or '')[:60]
    page_short.short_description = 'Page'


@admin.register(GSCPageStat)
class GSCPageStatAdmin(admin.ModelAdmin):
    list_display = ['date', 'page_short', 'clicks', 'impressions', 'ctr', 'position']
    list_filter = ['date']
    search_fields = ['page']
    date_hierarchy = 'date'

    def page_short(self, obj):
        return (obj.page or '')[:70]
    page_short.short_description = 'Page'


@admin.register(SerpSnapshot)
class SerpSnapshotAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'location', 'checked_at', 'our_domain_rank']
    list_filter = ['checked_at', 'keyword']
    search_fields = ['keyword', 'location']
    date_hierarchy = 'checked_at'


@admin.register(MetaAuditResult)
class MetaAuditResultAdmin(admin.ModelAdmin):
    list_display = ['url_short', 'checked_at', 'title_short', 'status_code', 'resp_ms', 'issues_display']
    list_filter = ['checked_at', 'status_code']
    search_fields = ['url', 'title', 'description']
    date_hierarchy = 'checked_at'

    def url_short(self, obj):
        return (obj.url or '')[:60]
    url_short.short_description = 'URL'

    def title_short(self, obj):
        return (obj.title or '')[:40]
    title_short.short_description = 'Title'

    def issues_display(self, obj):
        return ', '.join((obj.issues_json or [])[:5])
    issues_display.short_description = 'Issues'


@admin.register(InsightSession)
class InsightSessionAdmin(admin.ModelAdmin):
    list_display = ['sid', 'cid', 'first_seen', 'last_seen', 'consent']
    list_filter = ['consent', 'first_seen']
    search_fields = ['sid', 'cid']
    date_hierarchy = 'last_seen'
    readonly_fields = ['sid', 'first_seen', 'last_seen', 'ip_hash']


@admin.register(InsightEvent)
class InsightEventAdmin(admin.ModelAdmin):
    list_display = ['type', 'url_short', 'occurred_at', 'session']
    list_filter = ['type', 'occurred_at']
    search_fields = ['url', 'payload']
    date_hierarchy = 'occurred_at'

    def url_short(self, obj):
        return (obj.url or '')[:60]
    url_short.short_description = 'URL'


@admin.register(SEOHealthSnapshot)
class SEOHealthSnapshotAdmin(admin.ModelAdmin):
    list_display = ['snapshot_at', 'gsc_end_date', 'behavior_end_date']
    list_filter = ['snapshot_at']
    date_hierarchy = 'snapshot_at'
    readonly_fields = [
        'snapshot_at', 'gsc_start_date', 'gsc_end_date', 'behavior_start_date', 'behavior_end_date',
        'gsc_json', 'behavior_json', 'meta_issues_json', 'opportunities_json',
        'ux_issues_json', 'meta_issues_pages_json',
    ]

    def has_add_permission(self, request):
        return False


@admin.register(InsightAlert)
class InsightAlertAdmin(admin.ModelAdmin):
    list_display = ['rule_key', 'severity', 'message_short', 'created_at']
    list_filter = ['severity', 'rule_key', 'created_at']
    search_fields = ['message', 'rule_key']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

    def message_short(self, obj):
        return (obj.message or '')[:60]
    message_short.short_description = 'Message'
