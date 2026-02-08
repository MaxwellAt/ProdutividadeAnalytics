from django.core.management.base import BaseCommand
from dados_produtividade.etl.ingestors import MockIngestor

class Command(BaseCommand):
    help = 'Runs the ETL process to ingest mock data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting ETL...")
        ingestor = MockIngestor()
        ingestor.generate_data()
        self.stdout.write(self.style.SUCCESS("ETL Finished Successfully."))
