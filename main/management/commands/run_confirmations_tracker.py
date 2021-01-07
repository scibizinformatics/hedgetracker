from django.core.management.base import BaseCommand
from main.bchd import confirmations_tracker

class Command(BaseCommand):

    def handle(self, *args, **options):
        confirmations_tracker.run()
