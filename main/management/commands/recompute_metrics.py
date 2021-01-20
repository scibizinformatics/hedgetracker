from django.core.management.base import BaseCommand

from main.utils.metrics import MetricsHandler
from main.models import Settlement, Metric

from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):

    def handle(self, *args, **options):
        Metric.objects.all().delete()

        day = 10
        while day <= 20:
            start = datetime(year=2021, month=1, day=day, hour=23, minute=50, tzinfo=pytz.utc)
            end = datetime(year=2021, month=1, day=(day+1), hour=23, minute=50, tzinfo=pytz.utc)

            settlements = Settlement.objects.filter(
                block__timestamp__gt=start,
                block__timestamp__lt=end
            )

            m = MetricsHandler(settlements, end)
            m.compute_metrics()
            
            self.stdout.write(self.style.SUCCESS(f'Calculated metrics for day {day}'))
            day += 1

