"""
Management command to automatically translate all empty msgstr in .po files.
Uses deep-translator to translate from Turkish to target languages.
"""
import sys
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from deep_translator import GoogleTranslator
import polib


class Command(BaseCommand):
    help = 'Automatically translate all empty msgstr in .po files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force retranslate even if msgstr is not empty',
        )
        parser.add_argument(
            '--lang',
            type=str,
            help='Specific language to translate (fa, ar, tr, en). If not specified, translates all.',
        )

    def handle(self, *args, **options):
        # Fix encoding for Windows console
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

        force = options['force']
        target_lang = options.get('lang')
        
        locale_path = Path(settings.BASE_DIR) / 'locale'
        
        # Language mapping for Google Translator
        lang_map = {
            'fa': 'fa',
            'ar': 'ar',
            'tr': 'tr',
            'en': 'en',
        }
        
        # Source language (we'll translate from Turkish)
        source_lang = 'tr'
        
        languages = [target_lang] if target_lang else ['fa', 'ar', 'en']
        
        for lang_code in languages:
            if lang_code not in lang_map:
                self.stdout.write(self.style.WARNING(f'Skipping unknown language: {lang_code}'))
                continue
            
            po_file = locale_path / lang_code / 'LC_MESSAGES' / 'django.po'
            
            if not po_file.exists():
                self.stdout.write(self.style.WARNING(f'File not found: {po_file}'))
                continue
            
            self.stdout.write(f'\nProcessing: {po_file}')
            self.translate_po_file(po_file, source_lang, lang_map[lang_code], force)
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Translation completed!'))
        self.stdout.write('\nRun: python manage.py compilemessages')

    def translate_po_file(self, po_file, source_lang, target_lang, force=False):
        """Translate all empty msgstr in a .po file using polib"""
        try:
            # Try to read with error handling
            po = polib.pofile(str(po_file), check_for_duplicates=False)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error reading file (trying to fix): {e}'))
            # Try to fix common issues and read again
            try:
                # Read file as text and fix common issues
                with open(po_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Fix unescaped quotes (basic fix)
                content = content.replace('msgstr ""\nmsgstr "', 'msgstr "')
                # Write back
                with open(po_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                # Try reading again
                po = polib.pofile(str(po_file), check_for_duplicates=False)
            except Exception as e2:
                self.stdout.write(self.style.ERROR(f'Could not fix file: {e2}'))
                self.stdout.write(self.style.WARNING('  Run: python manage.py makemessages to regenerate .po files'))
                return
        
        translated_count = 0
        skipped_count = 0
        error_count = 0
        
        # Initialize translator
        if source_lang != target_lang:
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error initializing translator: {e}'))
                return
        
        for entry in po:
            # Skip metadata entries
            if entry.msgid == '':
                continue
            
            # Skip if already translated and force is False
            if entry.msgstr and not force:
                skipped_count += 1
                continue
            
            # Skip if text is too short
            if len(entry.msgid.strip()) < 2:
                continue
            
            # Skip if msgid starts/ends with newline (multiline) - these need special handling
            if entry.msgid.startswith('\n') or entry.msgid.endswith('\n'):
                continue
            
            # Skip if msgid contains Python format strings (%s, %d, etc.) - preserve format
            has_format = '%' in entry.msgid and ('%s' in entry.msgid or '%d' in entry.msgid or '%(' in entry.msgid)
            
            try:
                if source_lang == target_lang:
                    translated_text = entry.msgid
                else:
                    # Translate using GoogleTranslator
                    translated_text = translator.translate(entry.msgid)
                    # Add small delay to avoid rate limiting (reduced)
                    time.sleep(0.05)
                
                # If original had format strings, make sure they're preserved
                if has_format:
                    # Basic check: if format strings are missing, skip
                    original_formats = set(re.findall(r'%[sd]|%\([^)]+\)[sd]', entry.msgid))
                    translated_formats = set(re.findall(r'%[sd]|%\([^)]+\)[sd]', translated_text))
                    if original_formats != translated_formats:
                        # Format strings don't match, skip this translation
                        continue
                
                entry.msgstr = translated_text
                translated_count += 1
                
                if translated_count % 10 == 0:
                    self.stdout.write(f'  Translated {translated_count} strings...')
            
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Only show first 5 errors
                    self.stdout.write(self.style.WARNING(f'  Translation error: {str(e)[:100]}'))
                continue
        
        # Save the file
        try:
            po.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Translated: {translated_count} strings'))
            if skipped_count > 0:
                self.stdout.write(f'  - Skipped: {skipped_count} strings (already translated)')
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f'  - Errors: {error_count} strings'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  Error saving file: {e}'))
