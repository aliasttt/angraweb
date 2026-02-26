"""Tests for language-prefixed URL structure (tr/en) and language switching."""
from django.test import TestCase
from django.urls import reverse


class I18nURLTest(TestCase):
    """Verify /tr/ and /en/ routes work and return 200."""

    def test_tr_home_returns_200(self):
        response = self.client.get('/tr/')
        self.assertEqual(response.status_code, 200)

    def test_en_home_returns_200(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)

    def test_tr_about_returns_200(self):
        response = self.client.get('/tr/about/')
        self.assertEqual(response.status_code, 200)

    def test_en_about_returns_200(self):
        response = self.client.get('/en/about/')
        self.assertEqual(response.status_code, 200)

    def test_root_redirects_301_to_language_prefix(self):
        """Root / must redirect with 301 permanent to /tr/ or /en/."""
        response = self.client.get('/', follow=False)
        self.assertEqual(response.status_code, 301, msg='Root redirect should be 301 permanent')
        loc = response['Location']
        self.assertTrue(loc.endswith('/tr/') or loc.endswith('/en/'), msg=f'Expected .../tr/ or .../en/ got {loc}')

    def test_root_redirects_to_tr_when_no_cookie(self):
        """With no language cookie/session, / redirects to /tr/ (LANGUAGE_CODE)."""
        response = self.client.get('/', follow=False)
        self.assertEqual(response.status_code, 301)
        self.assertIn('/tr/', response['Location'], msg='Default language is tr')

    def test_reverse_index_includes_prefix_when_language_active(self):
        from django.utils import translation
        translation.activate('en')
        try:
            url = reverse('index')
            self.assertTrue(url.startswith('/en'), msg=f'Expected /en/... got {url}')
        finally:
            translation.deactivate()
        translation.activate('tr')
        try:
            url = reverse('index')
            self.assertTrue(url.startswith('/tr'), msg=f'Expected /tr/... got {url}')
        finally:
            translation.deactivate()


class LanguageSwitchTest(TestCase):
    """Verify switching language preserves path."""

    def test_switch_to_en_redirects_to_same_path_in_en(self):
        # From /tr/about/ with ?next=/tr/about/ → redirect to /en/about/
        response = self.client.get(
            '/lang/en/',
            {'next': 'http://testserver/tr/about/'},
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('/en/about/'), msg=response['Location'])

    def test_switch_to_tr_redirects_to_same_path_in_tr(self):
        response = self.client.get(
            '/lang/tr/',
            {'next': 'http://testserver/en/contact/'},
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('/tr/contact/'), msg=response['Location'])

    def test_switch_with_path_only_next(self):
        response = self.client.get('/lang/en/', {'next': '/tr/services/'}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('/en/services/'), msg=response['Location'])

    def test_invalid_lang_redirects_to_root(self):
        response = self.client.get('/lang/xx/', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'] in ('/', 'http://testserver/'), msg=response['Location'])


class I18nSEOTest(TestCase):
    """Verify canonical, hreflang, sitemap and that admin is not broken."""

    def test_tr_page_has_canonical_pointing_to_tr(self):
        response = self.client.get('/tr/services/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, '/tr/services/')

    def test_en_page_has_canonical_pointing_to_en(self):
        response = self.client.get('/en/services/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, '/en/services/')

    def test_tr_page_has_hreflang_tr_en_xdefault(self):
        response = self.client.get('/tr/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hreflang="tr"')
        self.assertContains(response, 'hreflang="en"')
        self.assertContains(response, 'hreflang="x-default"')

    def test_sitemap_xml_contains_tr_and_en_urls(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/tr/', response.content, msg='Sitemap should contain /tr/ URLs')
        self.assertIn(b'/en/', response.content, msg='Sitemap should contain /en/ URLs')

    def test_admin_path_not_broken(self):
        """Admin must remain at /admin/ and not be redirected to language prefix."""
        response = self.client.get('/admin/', follow=False)
        self.assertIn(response.status_code, (200, 302), msg='Admin should not return 404')
        if response.status_code == 302:
            self.assertIn('/admin/', response['Location'], msg='Redirect should stay in admin')

    def test_robots_txt_includes_sitemap(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sitemap:', response.content)
        self.assertIn(b'sitemap.xml', response.content)
