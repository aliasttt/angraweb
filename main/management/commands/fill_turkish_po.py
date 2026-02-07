# -*- coding: utf-8 -*-
"""Fill empty msgstr in Turkish .po by translating msgid (English) to Turkish.
Uses deep-translator (works on Python 3.11+ including 3.14; googletrans fails on 3.14).
"""
import re
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

try:
    import polib
except ImportError:
    polib = None

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None


def translate_text(text, max_length=4500):
    """Translate English text to Turkish. Split long text into chunks if needed."""
    if not text or not text.strip() or len(text) < 2:
        return text
    text = text.strip()
    # Google Translate free API has ~5000 char limit; use 4500 to be safe
    if len(text) <= max_length:
        try:
            return GoogleTranslator(source='en', target='tr').translate(text)
        except Exception:
            return None
    # Split by paragraphs or sentences and translate in chunks
    parts = re.split(r'\n\n+|\n', text)
    out = []
    chunk = []
    chunk_len = 0
    for p in parts:
        if chunk_len + len(p) + 2 > max_length and chunk:
            try:
                translated = GoogleTranslator(source='en', target='tr').translate('\n'.join(chunk))
                out.append(translated)
            except Exception:
                out.append('\n'.join(chunk))
            chunk = []
            chunk_len = 0
        chunk.append(p)
        chunk_len += len(p) + 1
    if chunk:
        try:
            translated = GoogleTranslator(source='en', target='tr').translate('\n'.join(chunk))
            out.append(translated)
        except Exception:
            out.append('\n'.join(chunk))
    return '\n\n'.join(out) if out else text


class Command(BaseCommand):
    help = 'Fill empty msgstr in locale/tr with Turkish (EN->TR) using deep-translator'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only show how many would be translated, do not save',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Also translate entries where msgstr equals msgid (still English)',
        )

    def handle(self, *args, **options):
        if not polib:
            self.stdout.write(self.style.ERROR('Need: pip install polib'))
            return
        if not GoogleTranslator:
            self.stdout.write(self.style.ERROR('Need: pip install deep-translator'))
            return

        po_path = Path(settings.BASE_DIR) / 'locale' / 'tr' / 'LC_MESSAGES' / 'django.po'
        if not po_path.exists():
            self.stdout.write(self.style.ERROR(f'Not found: {po_path}'))
            return

        po = polib.pofile(str(po_path), check_for_duplicates=False)
        translated_count = 0
        error_count = 0
        dry_run = options.get('dry_run', False)
        force = options.get('force', False)

        for entry in po:
            if not entry.msgid:
                continue
            has_content = entry.msgstr and entry.msgstr.strip()
            # If not --force, skip already translated
            if has_content and not force:
                continue
            # If --force, still skip when msgstr is already Turkish (different from msgid and not empty)
            if has_content and force and entry.msgstr.strip() != entry.msgid.strip():
                continue
            if not entry.msgid.strip():
                continue

            text = entry.msgid.strip() if (entry.msgid.startswith('\n') or entry.msgid.endswith('\n')) else entry.msgid
            if len(text) < 2:
                continue

            try:
                result = translate_text(text)
                if result is None:
                    error_count += 1
                    continue
                # In .po, literal % must be written as %%
                if '%' in result:
                    result = result.replace('%', '%%')
                # Multiline: msgstr must start/end with \n if msgid does (gettext requirement)
                if entry.msgid.startswith('\n'):
                    result = '\n' + result
                if entry.msgid.endswith('\n'):
                    result = result.rstrip()
                    if not result.endswith('\n'):
                        result = result + '\n'
                entry.msgstr = result
                translated_count += 1
                if translated_count % 10 == 0:
                    self.stdout.write(f'  {translated_count}...')
                time.sleep(0.08)
            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'Would translate {translated_count} strings. Errors: {error_count}'))
            return

        try:
            po.save()
            self.stdout.write(self.style.SUCCESS(f'Done. Translated {translated_count} strings. Errors: {error_count}'))
            self.stdout.write('Run: python manage.py compilemessages -l tr')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Save error: {e}'))
