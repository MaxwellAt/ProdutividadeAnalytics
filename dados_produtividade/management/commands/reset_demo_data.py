from django.core.management.base import BaseCommand
from django.core.management import call_command
from dados_produtividade.models import ActivityLog, Task, Category, Source, ClassificationRule

class Command(BaseCommand):
    help = 'Wipes operational data and regenerates demo data using ETL. Safe for existing schemas.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Cleaning up operational data...'))
        
        # Order matters for foreign keys
        ActivityLog.objects.all().delete()
        Task.objects.all().delete()
        # Optional: Keep categories/rules if you consider them config, not data.
        # For a full reset/demo mode, we usually wipe them too or ensure defaults exist.
        # ClassificationRule.objects.all().delete()
        # Category.objects.all().delete()
        # Source.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Data wiped successfully.'))

        self.stdout.write(self.style.NOTICE('Running ETL to generate fresh mock data...'))
        call_command('run_etl')
        
        self.stdout.write(self.style.SUCCESS('Reset process completed. System represents a fresh install with 30 days of mock history.'))
