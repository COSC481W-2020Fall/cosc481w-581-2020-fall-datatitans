from django.core.management.base import BaseCommand, CommandError
from data.scripts.database_handler import initialize_table


class Command(BaseCommand):
    help = "Populates the data table with covid data"

    def handle(self, *args, **options):
        initialize_table()
