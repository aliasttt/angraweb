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

    def test_root_redirects_to_language_prefix(self):
        response = self.client.get('/', follow=False)
        self.assertEqual(response.status_code, 302)
        loc = response['Location']
        self.assertTrue(loc.endswith('/tr/') or loc.endswith('/en/'), msg=f'Expected .../tr/ or .../en/ got {loc}')

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
