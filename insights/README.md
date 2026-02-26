# Insights App — SEO Dashboard & On-Site Behavior Analytics

Django app providing:

1. **SEO Data Dashboard** — Google Search Console (GSC), optional GA4, optional SERP snapshots (feature-flagged)
2. **On-Site User Behavior Analytics** — page views, scroll depth, clicks, sessions, funnels, alerts (internal tracking via JS + Django collect endpoint)

---

## Setup

### 1. Install dependencies

Already in project `requirements.txt`:

- `google-api-python-client` — GSC API
- `google-auth` — GSC/GA4 auth
- `requests` — SERP/meta audit

```bash
pip install -r requirements.txt
```

### 2. Migrate and static

```bash
python manage.py migrate
python manage.py collectstatic --noinput   # when deploying
```

### 3. Environment variables

Use env vars (or Django settings) for secrets. Optional vars have defaults or can be omitted.

#### Google Search Console (required for SEO sync)

Set in environment (or `angraweb_project/settings.py` reads from `os.environ`):

| Variable | Description |
|----------|-------------|
| `INSIGHTS_GSC_SITE_URL` | Property URL, e.g. `sc-domain:angraweb.com` or `https://example.com/` |
| `INSIGHTS_GSC_CREDENTIALS_JSON` | Path to service account JSON file, or JSON string |
| `INSIGHTS_GSC_DAYS_DEFAULT` | Default days to sync (default: `28`) |

**Smoke-test** (ensure env is loaded; run from project root with env vars set):

```bash
python manage.py shell -c "from django.conf import settings; print(settings.INSIGHTS_GSC_SITE_URL); print(bool(settings.INSIGHTS_GSC_CREDENTIALS_JSON))"
```

Expected with GSC configured: first line is site URL (e.g. `sc-domain:angraweb.com`), second is `True`.

#### Optional: GA4

| Variable | Description |
|----------|-------------|
| `INSIGHTS_GA4_PROPERTY_ID` | GA4 property ID |
| `INSIGHTS_GA4_CREDENTIALS_JSON` | Service account JSON path or string |

#### Optional: SERP (feature-flagged)

| Variable | Description |
|----------|-------------|
| `INSIGHTS_ENABLE_SERP` | `1` to enable SERP snapshots |
| `INSIGHTS_SERPAPI_KEY` | SerpApi key |
| `INSIGHTS_SERP_LOCATION` | e.g. `Istanbul, Turkey` |
| `INSIGHTS_SERP_KEYWORDS` | Comma-separated keywords |

#### Behavior analytics (collect endpoint)

| Variable | Description |
|----------|-------------|
| `INSIGHTS_COLLECT_ALLOWED_ORIGINS` | Comma-separated origins (e.g. `https://example.com`). Empty = permissive in dev. |
| `INSIGHTS_COLLECT_ALLOWED_HOSTS` | Comma-separated Host values. Defaults to `ALLOWED_HOSTS`. |
| `INSIGHTS_REQUIRE_CONSENT` | `1` (default) = tracking only after consent; `0` = track without consent (e.g. non-EU). |
| `INSIGHTS_RESPECT_DNT` | `1` = respect Do Not Track; `0` (default) = ignore DNT. |
| `INSIGHTS_FUNNEL_STEPS` | Comma-separated URL path prefixes for funnel, e.g. `/,/packages/,/contact/,/quote/` |

---

## Running

### Sync GSC (cron recommended)

```bash
python manage.py insights_sync_gsc --days 28
```

### Optional: GA4

```bash
python manage.py insights_sync_ga4 --days 28
```

### Meta audit (sitemap)

```bash
python manage.py insights_audit_meta --sitemap https://example.com/sitemap.xml --max-pages 200
```

### Include tracker on site pages

The tracker is already included in `templates/base.html`:

- `{% static 'insights/tracker.js' %}` — behavior tracker
- `{% static 'insights/consent.css' %}` and `{% static 'insights/consent.js' %}` — consent banner

If you use a different base template, add:

```html
<script>
  window.INSIGHTS_COLLECT_URL = "{% url 'insights:collect' %}";
  window.INSIGHTS_REQUIRE_CONSENT = true;  /* set false to skip consent (non-EU) */
  window.INSIGHTS_RESPECT_DNT = false;
</script>
<script src="{% static 'insights/tracker.js' %}"></script>
<link rel="stylesheet" href="{% static 'insights/consent.css' %}">
<script src="{% static 'insights/consent.js' %}"></script>
```

### Open the dashboard

- **Insights dashboard (staff only):** [https://your-domain/admin/insights/](https://your-domain/admin/insights/)
- **Django Admin models:** `/admin/` → Insights (GSC stats, SERP, Meta audit, Sessions, Events)

---

## Consent (EU / privacy)

- **Consent required (default):** `INSIGHTS_REQUIRE_CONSENT=1` — no tracking until the user clicks “Accept” in the banner. Use this for EU/EEA or strict privacy.
- **No consent required:** `INSIGHTS_REQUIRE_CONSENT=0` — tracker runs for everyone; banner can still be shown for notice-only.
- **Do Not Track:** `INSIGHTS_RESPECT_DNT=1` — if the browser sends `DNT: 1`, the tracker does not send events.

---

## Security

- Collect endpoint: rate limit per IP (cache-based), optional origin/host allowlist, payload size limit, max events per request (20).
- IPs are hashed before storage (`ip_hash`); raw IP is not stored.
- Use HTTPS and set `INSIGHTS_COLLECT_ALLOWED_ORIGINS` / `INSIGHTS_COLLECT_ALLOWED_HOSTS` in production.

---

## Tests

```bash
python manage.py test insights.tests
```

---

## Clear all data (only real data)

To remove all Insights data (including any sample/demo data) and use only real data:

```bash
python manage.py insights_clear_data
```

Type `yes` when asked. To skip confirmation (e.g. in scripts):

```bash
python manage.py insights_clear_data --no-input
```

After that, data will come only from:
- **GSC:** `insights_sync_gsc`
- **Behavior:** real site visits (tracker + consent)
- **Meta:** `insights_audit_meta`
- **SERP:** SERP sync (if enabled)

The command `insights_load_sample_data` is only for demo; do not run it if you want only real data.

---

## App structure

- `insights/models.py` — GSC, SERP, MetaAudit, InsightSession, InsightEvent
- `insights/services/gsc.py` — GSC API sync
- `insights/services/ga4.py` — GA4 stub
- `insights/services/serp.py` — SERP snapshots (feature flag)
- `insights/services/analytics_ingest.py` — collect validation and process_events
- `insights/services/analytics_reports.py` — behavior aggregations
- `insights/services/gsc_reports.py` — GSC KPIs and alerts
- `insights/views.py` — POST `/insights/collect/`
- `insights/views_admin.py` — dashboard view
- `insights/management/commands/` — insights_sync_gsc, insights_sync_ga4, insights_audit_meta
- `static/insights/tracker.js` — client-side tracker
- `static/insights/consent.js` + `consent.css` — consent banner
