# -*- coding: utf-8 -*-
"""Translate all localized model content (title, description, etc.) to Turkish.
Site is Turkish-only; for lang 'tr' the template uses the base field, so we set it to Turkish.
"""
import time
from django.core.management.base import BaseCommand
from django.apps import apps
from main.models import (
    Service, Project, ProjectVideo, BlogPost, Testimonial, FAQ,
    ProcessStep, CaseStudy, TimelineEvent, Skill, Certificate,
)

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

MAX_LEN = 4500


def translate_to_tr(text):
    if not text or not str(text).strip() or len(str(text).strip()) < 2:
        return text
    text = str(text).strip()
    try:
        if len(text) <= MAX_LEN:
            return GoogleTranslator(source='auto', target='tr').translate(text)
        parts = []
        for i in range(0, len(text), MAX_LEN):
            chunk = text[i:i + MAX_LEN]
            parts.append(GoogleTranslator(source='auto', target='tr').translate(chunk))
            time.sleep(0.1)
        return ' '.join(parts)
    except Exception:
        return text


class Command(BaseCommand):
    help = 'Translate all model content (Service, FAQ, Blog, etc.) to Turkish for Turkish-only site'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only show counts, do not save')

    def handle(self, *args, **options):
        if not GoogleTranslator:
            self.stdout.write(self.style.ERROR('Need: pip install deep-translator'))
            return
        dry_run = options.get('dry_run', False)

        # (Model, list of base field names used for 'tr' in templates)
        to_translate = [
            (Service, ['title', 'description']),
            (Project, ['title', 'description']),
            (ProjectVideo, ['title', 'description']),
            (BlogPost, ['title', 'excerpt', 'content']),
            (Testimonial, ['content']),
            (FAQ, ['question', 'answer']),
            (ProcessStep, ['title', 'description']),
            (CaseStudy, ['title', 'challenge', 'solution', 'results']),
            (TimelineEvent, ['title', 'description']),
            (Skill, ['name']),
            (Certificate, ['title', 'description']),
        ]
        total = 0
        for model, fields in to_translate:
            qs = model.objects.all()
            for obj in qs:
                updated = False
                for field in fields:
                    if not hasattr(obj, field):
                        continue
                    val = getattr(obj, field)
                    if not val or not str(val).strip():
                        continue
                    tr = translate_to_tr(val)
                    if tr and tr != val:
                        if not dry_run:
                            setattr(obj, field, tr)
                        updated = True
                        total += 1
                if updated and not dry_run:
                    obj.save()
                if updated:
                    time.sleep(0.08)
        self.stdout.write(self.style.SUCCESS(
            f'{"Would translate" if dry_run else "Translated"} {total} field(s) to Turkish.'
        ))
