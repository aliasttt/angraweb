"""
Models for SEO data (GSC, SERP, meta audit) and on-site behavior analytics.
"""
import uuid
from django.db import models
from django.utils import timezone


# ─── Google Search Console ───────────────────────────────────────────────────

class GSCQueryPageStat(models.Model):
    """Daily GSC stats by query + page. Unique on (date, query, page)."""
    date = models.DateField(db_index=True)
    query = models.CharField(max_length=500, db_index=True)
    page = models.URLField(max_length=2048, db_index=True)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    ctr = models.FloatField(default=0.0)  # 0–1 or percentage depending on API
    position = models.FloatField(default=0.0)

    class Meta:
        db_table = 'insights_gsc_query_page_stat'
        verbose_name = 'GSC Query+Page Stat'
        verbose_name_plural = 'GSC Query+Page Stats'
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'query', 'page'],
                name='insights_gsc_qp_unique',
            ),
        ]
        indexes = [
            models.Index(fields=['date', 'query']),
            models.Index(fields=['date', 'page']),
        ]
        ordering = ['-date', '-clicks']

    def __str__(self):
        return f'{self.date} | {self.query[:40]} | {self.page[:40]}'


class GSCPageStat(models.Model):
    """Daily GSC stats by page only. Unique on (date, page)."""
    date = models.DateField(db_index=True)
    page = models.URLField(max_length=2048, db_index=True)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    ctr = models.FloatField(default=0.0)
    position = models.FloatField(default=0.0)

    class Meta:
        db_table = 'insights_gsc_page_stat'
        verbose_name = 'GSC Page Stat'
        verbose_name_plural = 'GSC Page Stats'
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'page'],
                name='insights_gsc_page_unique',
            ),
        ]
        indexes = [
            models.Index(fields=['date', 'page']),
        ]
        ordering = ['-date', '-clicks']

    def __str__(self):
        return f'{self.date} | {self.page[:60]}'


# ─── SERP snapshots (optional, feature-flagged) ──────────────────────────────

class SerpSnapshot(models.Model):
    """SERP snapshot for a keyword: top 10 organic results + our rank."""
    keyword = models.CharField(max_length=255, db_index=True)
    location = models.CharField(max_length=255, default='')
    checked_at = models.DateTimeField(db_index=True, default=timezone.now)
    results_json = models.JSONField(default=dict)  # list of {position, title, url, ...}
    our_domain_rank = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'insights_serp_snapshot'
        verbose_name = 'SERP Snapshot'
        verbose_name_plural = 'SERP Snapshots'
        ordering = ['-checked_at']

    def __str__(self):
        return f'{self.keyword} @ {self.checked_at.date()} (rank={self.our_domain_rank})'


# ─── Meta audit (SEO meta tags) ─────────────────────────────────────────────

class MetaAuditResult(models.Model):
    """Crawled page meta audit: title, description, h1, canonical, status."""
    url = models.URLField(max_length=2048, db_index=True)
    checked_at = models.DateTimeField(db_index=True, default=timezone.now)
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    h1_count = models.PositiveIntegerField(default=0)
    canonical = models.URLField(max_length=2048, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    resp_ms = models.PositiveIntegerField(null=True, blank=True)  # response time ms
    issues_json = models.JSONField(default=list)  # list of issue strings

    class Meta:
        db_table = 'insights_meta_audit_result'
        verbose_name = 'Meta Audit Result'
        verbose_name_plural = 'Meta Audit Results'
        ordering = ['-checked_at']

    def __str__(self):
        return f'{self.url[:50]} @ {self.checked_at.date()} ({self.status_code})'


# ─── On-site behavior analytics ────────────────────────────────────────────

class InsightSession(models.Model):
    """Anonymous session for behavior tracking."""
    sid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    cid = models.CharField(max_length=64, blank=True, db_index=True)  # optional client id
    first_seen = models.DateTimeField(default=timezone.now, db_index=True)
    last_seen = models.DateTimeField(default=timezone.now, db_index=True)
    user_agent = models.CharField(max_length=512, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True, db_index=True)  # hashed IP, no raw IP
    referrer = models.URLField(max_length=2048, blank=True)
    consent = models.BooleanField(default=False)

    class Meta:
        db_table = 'insights_session'
        verbose_name = 'Insight Session'
        verbose_name_plural = 'Insight Sessions'
        ordering = ['-last_seen']

    def __str__(self):
        return str(self.sid)


class InsightEvent(models.Model):
    """Single behavior event: page_view, scroll_depth, click, page_exit, rage_click."""
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('scroll_depth', 'Scroll Depth'),
        ('click', 'Click'),
        ('page_exit', 'Page Exit'),
        ('rage_click', 'Rage Click'),
    ]
    session = models.ForeignKey(
        InsightSession,
        on_delete=models.CASCADE,
        related_name='events',
        db_index=True,
    )
    type = models.CharField(max_length=20, choices=EVENT_TYPES, db_index=True)
    url = models.URLField(max_length=2048, blank=True, db_index=True)
    occurred_at = models.DateTimeField(db_index=True, default=timezone.now)
    payload = models.JSONField(default=dict)

    class Meta:
        db_table = 'insights_event'
        verbose_name = 'Insight Event'
        verbose_name_plural = 'Insight Events'
        indexes = [
            models.Index(fields=['type', 'occurred_at']),
            models.Index(fields=['url', 'occurred_at']),
        ]
        ordering = ['-occurred_at']

    def __str__(self):
        return f'{self.type} @ {self.url[:40]} @ {self.occurred_at}'
