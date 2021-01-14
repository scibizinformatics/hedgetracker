from django.db.models.signals import post_migrate
from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals
        post_migrate.connect(self.run_txn_tracker, sender=self)


    def run_txn_tracker(self, *args, **kwargs):
        from main.bchd import transactions_tracker
        transactions_tracker.run()
