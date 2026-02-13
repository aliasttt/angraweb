"""
Management command to update project order:
1. firmentshirt (order: 1)
2. mybonusberlin (order: 2)
3. kanoonhamyari (order: 3)
4. pierinsaat (order: 4)
5. kalicimakyajmonir (order: 5)
6. angraweb (order: 6)
7. hedef surucu kursu (order: 7)
"""
import sys
from django.core.management.base import BaseCommand
from main.models import Project


class Command(BaseCommand):
    help = 'Update final project order'

    def handle(self, *args, **options):
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        projects_order = [
            {'slug': 'firmentshirt-custom-tshirt-printing', 'order': 1},
            {'slug': 'bonus-berlin-qr-menu-loyalty', 'order': 2},
            {'slug': 'kanoon-hamyari-persian-community', 'order': 3},
            {'slug': 'pier-insaat-construction', 'order': 4},
            {'slug': 'kalici-makyaj-monir-permanent-makeup', 'order': 5},
            {'slug': 'angraweb-portfolio', 'order': 6},
            {'slug': 'hedef-surucu-kursu-driving-school', 'order': 7},
            {'slug': 'gezgin-ustalar-home-services', 'order': 8},  # Last
        ]

        updated_count = 0
        for project_data in projects_order:
            try:
                project = Project.objects.filter(slug=project_data['slug']).first()
                if project:
                    project.order = project_data['order']
                    project.save()
                    updated_count += 1
                    print(f'[+] Updated: {project.title[:50]} (order: {project_data["order"]})')
                else:
                    print(f'[~] Project not found: {project_data["slug"]}')
            except Exception as e:
                print(f'[!] Error updating {project_data["slug"]}: {e}')

        print(f'\n[OK] Updated {updated_count} projects!')
