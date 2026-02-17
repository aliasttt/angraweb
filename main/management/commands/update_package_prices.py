from django.core.management.base import BaseCommand
from main.models import Package


class Command(BaseCommand):
    help = 'Update package prices: Basic 8000, Commercial 15000, Professional 35000 and rename Professional to E-commerce'

    def handle(self, *args, **options):
        # Update Basic Package: 5000 → 8000
        try:
            basic = Package.objects.get(package_type='basic')
            basic.price = 8000
            basic.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Basic Package price updated: 8000 TL'))
        except Package.DoesNotExist:
            self.stdout.write(self.style.WARNING('Basic Package not found'))

        # Update Commercial Package: 10000 → 15000
        try:
            commercial = Package.objects.get(package_type='commercial')
            commercial.price = 15000
            commercial.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Commercial Package price updated: 15000 TL'))
        except Package.DoesNotExist:
            self.stdout.write(self.style.WARNING('Commercial Package not found'))

        # Update Professional Package: 15000 → 35000 and rename
        try:
            professional = Package.objects.get(package_type='professional')
            professional.price = 35000
            professional.title = 'E-Ticaret Web Sitesi'
            professional.title_en = 'E-commerce Website'
            professional.title_fa = 'وبسایت فروشگاهی'
            professional.title_ar = 'موقع التجارة الإلكترونية'
            professional.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Professional Package updated: 35000 TL, renamed to "E-Ticaret Web Sitesi"'))
        except Package.DoesNotExist:
            self.stdout.write(self.style.WARNING('Professional Package not found'))

        self.stdout.write(self.style.SUCCESS('\n✅ All package prices updated successfully!'))
