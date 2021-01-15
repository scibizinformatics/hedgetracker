from django.core.management.base import BaseCommand
from main.bchd import transactions_tracker


class Command(BaseCommand):

    def handle(self, *args, **options):
        transactions_tracker.run()
