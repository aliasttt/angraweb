"""
Management command to:
1. Delete "Proje Örnekleri" project
2. Update project order
3. Add screenshot URLs to projects using screenshot API
"""
import sys
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from main.models import Project


class Command(BaseCommand):
    help = 'Update project order and add screenshots'

    def handle(self, *args, **options):
        # Fix encoding for Windows console
        if sys.platform == 'win32':
            import codecs
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        # 1. Delete "Proje Örnekleri" project
        deleted_count = 0
        try:
            project_samples = Project.objects.filter(slug='project-samples')
            count = project_samples.count()
            if count > 0:
                project_samples.delete()
                deleted_count = count
                print(f'[+] Deleted {deleted_count} project(s): Proje Örnekleri')
            else:
                print('[~] Project "Proje Örnekleri" not found (may already be deleted)')
        except Exception as e:
            print(f'[!] Error deleting project: {e}')

        # 2. Define project order and screenshot URLs
        # Using screenshotapi.net free service (or you can use other services)
        projects_order = [
            {
                'slug': 'firmentshirt-custom-tshirt-printing',
                'order': 1,
                'domain': 'firmentshirt.shop',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://www.firmentshirt.shop&width=1920&height=1080&format=png'
            },
            {
                'slug': 'bonus-berlin-qr-menu-loyalty',
                'order': 2,
                'domain': 'mybonusberlin.de',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://mybonusberlin.de&width=1920&height=1080&format=png'
            },
            {
                'slug': 'kanoon-hamyari-persian-community',
                'order': 3,
                'domain': 'kanoonhamyari.com',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://kanoonhamyari.com&width=1920&height=1080&format=png'
            },
            {
                'slug': 'gezgin-ustalar-home-services',
                'order': 4,
                'domain': 'gezginustalar.com',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://gezginustalar.com&width=1920&height=1080&format=png'
            },
            {
                'slug': 'pier-insaat-construction',
                'order': 5,
                'domain': 'pierinsaat.com',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://pierinsaat.com&width=1920&height=1080&format=png'
            },
            {
                'slug': 'kalici-makyaj-monir-permanent-makeup',
                'order': 6,
                'domain': 'kalicimakyajmonir.com.tr',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://kalicimakyajmonir.com.tr&width=1920&height=1080&format=png'
            },
            {
                'slug': 'angraweb-portfolio',
                'order': 7,
                'domain': 'angraweb.com',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://angraweb.com&width=1920&height=1080&format=png'
            },
            {
                'slug': 'hedef-surucu-kursu-driving-school',
                'order': 8,
                'domain': 'hedefsürücükursları.com.tr',
                'screenshot_url': 'https://api.screenshotapi.net/screenshot?url=https://xn--hedefsrckurslar-4vbbb82h.com.tr&width=1920&height=1080&format=png'
            },
        ]

        # 3. Update order for each project
        updated_count = 0
        for project_data in projects_order:
            try:
                project = Project.objects.filter(slug=project_data['slug']).first()
                if project:
                    old_order = project.order
                    project.order = project_data['order']
                    project.save()
                    updated_count += 1
                    print(f'[+] Updated: {project.title[:50]} (order: {old_order} -> {project_data["order"]})')
                else:
                    print(f'[~] Project not found: {project_data["slug"]}')
            except Exception as e:
                print(f'[!] Error updating {project_data["slug"]}: {e}')

        print(f'\n[OK] Completed! Deleted: {deleted_count}, Updated: {updated_count}')
        print('\nNote: Screenshots will be loaded dynamically from screenshot API in the template.')
