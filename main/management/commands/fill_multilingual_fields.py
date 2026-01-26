"""
Management command to fill multilingual fields from base fields.
If a multilingual field (title_fa, description_fa, etc.) is empty,
it will be filled with the base field (title, description) as fallback.
"""
import sys
from django.core.management.base import BaseCommand
from main.models import Service, Package, Project, PackageFeature


class Command(BaseCommand):
    help = 'Fill empty multilingual fields with base fields as fallback'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if multilingual field is not empty',
        )

    def handle(self, *args, **options):
        # Fix encoding for Windows console
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
        force = options['force']
        updated_count = {
            'services': 0,
            'packages': 0,
            'projects': 0,
            'features': 0,
        }

        # Update Services
        self.stdout.write('Updating Services...')
        for service in Service.objects.all():
            updated = False
            
            # Title fields
            if not service.title_fa or force:
                service.title_fa = service.title
                updated = True
            if not service.title_en or force:
                service.title_en = service.title
                updated = True
            if not service.title_ar or force:
                service.title_ar = service.title
                updated = True
            
            # Description fields
            if not service.description_fa or force:
                service.description_fa = service.description
                updated = True
            if not service.description_en or force:
                service.description_en = service.description
                updated = True
            if not service.description_ar or force:
                service.description_ar = service.description
                updated = True
            
            if updated:
                service.save()
                updated_count['services'] += 1
                try:
                    self.stdout.write(f'  [OK] Updated: {service.title}')
                except UnicodeEncodeError:
                    self.stdout.write(f'  [OK] Updated: Service ID {service.id}')

        # Update Packages
        self.stdout.write('\nUpdating Packages...')
        for package in Package.objects.all():
            updated = False
            
            # Title fields
            if not package.title_fa or force:
                package.title_fa = package.title
                updated = True
            if not package.title_en or force:
                package.title_en = package.title
                updated = True
            if not package.title_ar or force:
                package.title_ar = package.title
                updated = True
            
            # Description fields
            if package.description:  # Only if description exists
                if not package.description_fa or force:
                    package.description_fa = package.description
                    updated = True
                if not package.description_en or force:
                    package.description_en = package.description
                    updated = True
                if not package.description_ar or force:
                    package.description_ar = package.description
                    updated = True
            
            if updated:
                package.save()
                updated_count['packages'] += 1
                try:
                    self.stdout.write(f'  [OK] Updated: {package.title}')
                except UnicodeEncodeError:
                    self.stdout.write(f'  [OK] Updated: Package ID {package.id}')

        # Update Projects
        self.stdout.write('\nUpdating Projects...')
        for project in Project.objects.all():
            updated = False
            
            # Title fields
            if not project.title_fa or force:
                project.title_fa = project.title
                updated = True
            if not project.title_en or force:
                project.title_en = project.title
                updated = True
            if not project.title_ar or force:
                project.title_ar = project.title
                updated = True
            
            # Description fields
            if not project.description_fa or force:
                project.description_fa = project.description
                updated = True
            if not project.description_en or force:
                project.description_en = project.description
                updated = True
            if not project.description_ar or force:
                project.description_ar = project.description
                updated = True
            
            if updated:
                project.save()
                updated_count['projects'] += 1
                try:
                    self.stdout.write(f'  [OK] Updated: {project.title}')
                except UnicodeEncodeError:
                    self.stdout.write(f'  [OK] Updated: Project ID {project.id}')

        # Update PackageFeatures
        self.stdout.write('\nUpdating Package Features...')
        for feature in PackageFeature.objects.all():
            updated = False
            
            # Title fields
            if not feature.title_fa or force:
                feature.title_fa = feature.title
                updated = True
            if not feature.title_en or force:
                feature.title_en = feature.title
                updated = True
            if not feature.title_ar or force:
                feature.title_ar = feature.title
                updated = True
            
            if updated:
                feature.save()
                updated_count['features'] += 1
                try:
                    self.stdout.write(f'  [OK] Updated: Feature ID {feature.id}')
                except UnicodeEncodeError:
                    self.stdout.write(f'  [OK] Updated: Feature ID {feature.id}')

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Summary:'))
        self.stdout.write(f'  Services updated: {updated_count["services"]}')
        self.stdout.write(f'  Packages updated: {updated_count["packages"]}')
        self.stdout.write(f'  Projects updated: {updated_count["projects"]}')
        self.stdout.write(f'  Features updated: {updated_count["features"]}')
        total = sum(updated_count.values())
        self.stdout.write(self.style.SUCCESS(f'\nTotal items updated: {total}'))
        self.stdout.write('\nNote: Multilingual fields are now filled with base fields as fallback.')
        self.stdout.write('You can manually edit them in Admin Panel to provide proper translations.')
