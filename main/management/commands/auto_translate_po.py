"""
Management command to automatically translate all empty msgstr in .po files.
Uses googletrans (free, no API key needed) to translate from Turkish to target languages.
"""
import sys
import time
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from googletrans import Translator
import polib


class Command(BaseCommand):
    help = 'Automatically translate all empty msgstr in .po files using Google Translate (free)'

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
        """Translate all empty msgstr in a .po file using polib and googletrans"""
        try:
            po = polib.pofile(str(po_file), check_for_duplicates=False)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file: {e}'))
            self.stdout.write(self.style.WARNING('  Run: python manage.py makemessages to regenerate .po files'))
            return
        
        translated_count = 0
        skipped_count = 0
        error_count = 0
        
        # Initialize translator (googletrans is free, no API key needed)
        translator = Translator()
        
        for entry in po:
            # Skip metadata entries
            if entry.msgid == '':
                continue
            
            # Check if msgstr is empty or just whitespace
            # polib returns empty string for msgstr "" in .po file
            msgstr_empty = not entry.msgstr or not entry.msgstr.strip()
            
            # Debug: show first empty entry
            if msgstr_empty and translated_count == 0:
                self.stdout.write(f'  Found empty msgstr: {entry.msgid[:60]}...')
            
            # Skip if already translated (has content) and force is False
            if not msgstr_empty and not force:
                skipped_count += 1
                continue
            
            # Skip if text is too short
            if len(entry.msgid.strip()) < 2:
                continue
            
            # Handle multiline strings (blocktrans entries)
            is_multiline = entry.msgid.startswith('\n') or entry.msgid.endswith('\n')
            text_to_translate = entry.msgid.strip() if is_multiline else entry.msgid
            
            # Check for format strings
            has_format = '%' in entry.msgid and ('%s' in entry.msgid or '%d' in entry.msgid or '%(' in entry.msgid)
            
            try:
                if source_lang == target_lang:
                    translated_text = entry.msgid
                else:
                    # Translate using googletrans (free, no API key)
                    result = translator.translate(text_to_translate, src=source_lang, dest=target_lang)
                    translated_text = result.text
                    
                    # Small delay to avoid rate limiting (reduced for speed)
                    time.sleep(0.02)
                    
                    # If it was multiline, preserve the format
                    if is_multiline:
                        # Keep the original newline structure
                        translated_text = '\n' + translated_text + '\n'
                
                # If original had format strings, make sure they're preserved
                if has_format:
                    # Extract format strings from original
                    original_formats = re.findall(r'%[sd]|%\([^)]+\)[sd]', entry.msgid)
                    translated_formats = re.findall(r'%[sd]|%\([^)]+\)[sd]', translated_text)
                    
                    # If format strings don't match, try to preserve them
                    if len(original_formats) != len(translated_formats):
                        # Try to fix: replace format strings in translation with original ones
                        for i, fmt in enumerate(original_formats):
                            if i < len(translated_formats):
                                translated_text = translated_text.replace(translated_formats[i], fmt, 1)
                
                entry.msgstr = translated_text
                translated_count += 1
                
                if translated_count % 10 == 0:
                    self.stdout.write(f'  Translated {translated_count} strings...')
            
            except Exception as e:
                error_count += 1
                if error_count <= 10:  # Show first 10 errors
                    error_msg = str(e)
                    if len(error_msg) > 100:
                        error_msg = error_msg[:100] + '...'
                    self.stdout.write(self.style.WARNING(f'  Translation error: {error_msg}'))
                # Continue with next entry
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
