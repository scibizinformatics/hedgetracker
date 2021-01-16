from django.core.management.base import BaseCommand

from main.bchd import transactions_tracker
from main.models import Funding


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fetching funding transactions with no transaction block...'))
        funding_txns_with_empty_block = Funding.objects.filter(
            transaction_block__isnull=True
        )
        count = 0
        for funding_txn in funding_txns_with_empty_block:
            block = transactions_tracker.get_funding_txn_block(funding_txn.transaction)
            Funding.objects.filter(id=funding_txn.id).update(
                transaction_block=block
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Filled blocks of {count} funding transactions.'))
