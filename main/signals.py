from django.db.models.signals import post_save
from django.conf import settings

from main.utils.metrics import MetricsHandler
from main.utils.alert import send_rt_data
from main.models import *
from main.serializers import (
    SettlementSerializer,
    MetricSerializer,
)
from main.helpers import (
    ts_to_date, 
    get_BCH_USD_price,
    get_block_info,
)

import requests


def associate_block(sender, instance, created=False, **kwargs):
    block_check = Block.objects.filter(height=instance.maturity_height)
    if block_check.exists():
        instance.maturity_block = block_check.first()
    else:
        height, timestamp = get_block_info(height=instance.maturity_height)
        block = Block(
            height=instance.maturity_height,
            timestamp=ts_to_date(timestamp)
        )
        block.save()
        instance.maturity_block = block
    instance.save()


def save_bch_usd_price(sender, instance, created=False, **kwargs):
    if created:
        price = get_BCH_USD_price()
        instance.bch_usd_price = price
        instance.save()


def compute_metrics(sender, instance, created=False, **kwargs):
    if created:
        metric_handler = MetricsHandler(instance.id)
        metric_handler.compute_metrics()

        # send new settlement txn data to front end through websocket
        send_rt_data(
            settings.OPERATIONS['SETTLEMENT'],
            SettlementSerializer(instance)
        )


def send_metric_data(sender, instance, created=False, **kwargs):
    if created:
        send_rt_data(
            settings.OPERATIONS['METRIC'],
            MetricSerializer(instance)
        )


post_save.connect(associate_block, sender=Funding)
post_save.connect(save_bch_usd_price, sender=Block)
post_save.connect(compute_metrics, sender=Settlement)
post_save.connect(send_metric_data, sender=Metric)
