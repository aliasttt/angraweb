# Language-prefixed URLs (SEO i18n) — migration notes

## Summary

The site now uses **language-prefixed URLs** for SEO:

- **/tr/** — Turkish
- **/en/** — English

Both prefixes are always used (no "default language without prefix"). The root `/` redirects to `/tr/` or `/en/` based on cookie/session or `LANGUAGE_CODE`.

## What changed

### URLs

- **Main app** routes are under `i18n_patterns` with `prefix_default_language=True`, so every page has an explicit `/tr/...` or `/en/...` URL.
- **Non-prefixed** (unchanged): `/admin/`, `/insights/`, `/lang/<code>/`, `/i18n/`, static/media.
- **Root** `/` → 302 to `/tr/` or `/en/` (from cookie/session or default).

### Language switcher

- Links use `{% url 'switch_lang' 'tr' %}?next={{ request.get_full_path|urlencode }}` (and same for `en`).
- The `set_language` view redirects to the **same path in the other language** (e.g. `/tr/about/` → `/en/about/`).

### Templates

- **base.html**
  - `<html lang="{{ request.LANGUAGE_CODE|default:'tr' }}">`
  - **Canonical**: `{{ canonical_url }}` (includes language prefix).
  - **hreflang**: `hreflang_urls` from context (tr, en, x-default) only on language-prefixed pages.
- All `{% url '...' %}` and `reverse()` in views use the **current request language** when under i18n, so links stay in the same language.

### Settings

- `USE_I18N = True`
- `LANGUAGES = [('tr', 'Turkish'), ('en', 'English')]`
- `LANGUAGE_COOKIE_NAME`, `LANGUAGE_SESSION_KEY` set.
- `LocaleMiddleware` remains after `SessionMiddleware`; `LanguageActivationMiddleware` only sets language from session/cookie for **non-prefixed** paths (e.g. `/admin/`).

### Sitemap

- `sitemap.xml` lists each logical page **twice**: once under `/tr/...` and once under `/en/...`, so search engines see both language versions.

### Old .html URLs

- Requests like `/tr/index.html`, `/en/about.html` 301 redirect to the corresponding language-prefixed path (e.g. `/tr/`, `/tr/about/`) using the current language from the URL.

## Template changes you might need

1. **Custom templates** that build links by string concatenation (e.g. `href="/about/"`) should use `{% url 'about' %}` so the correct `/tr/` or `/en/` prefix is used.
2. **Redirects** that pointed to `/` or `/about/` should point to a **named URL** (e.g. `redirect(reverse('index'))`) so the redirect keeps the current language.
3. **Canonical / hreflang**: Rely on the `canonical_url` and `hreflang_urls` context from `main.context_processors.canonical_url`; no need to duplicate in other templates unless you override the meta block.

## Compatibility with existing SEO meta

- Canonical URLs include the language prefix (e.g. `https://example.com/tr/about/`).
- hreflang tags are output only on language-prefixed pages; `x-default` points to the default language (tr).
- Existing meta (description, robots, OG, etc.) are unchanged; they still use `{% trans %}` and request context.

## Tests

- `main.tests_i18n_urls`: `/tr/` and `/en/` return 200, root redirects to a language prefix, `reverse('index')` includes prefix when language is active, and language switch redirects preserve path.

## Commit

Suggested message: **Implement full SEO language-prefixed URL structure (tr/en)**
