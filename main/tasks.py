from __future__ import absolute_import, unicode_literals
from celery import shared_task

from main.utils.metrics import MetricsHandler
from main.models import Settlement

from django.utils import timezone

from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(queue='metrics')
def compute_metrics():
    logger.info('COMPUTING METRICS...')
    day_ago = timezone.now() - timedelta(hours=24)
    settlements = Settlement.objects.filter(block__timestamp__gte=day_ago)
    m = MetricsHandler(settlements)
    m.compute_metrics()
