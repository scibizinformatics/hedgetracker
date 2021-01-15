from django.db.models.signals import post_save
from django.conf import settings

from main.models import Funding, Block
from main.utils import (
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


post_save.connect(associate_block, sender=Funding)
post_save.connect(save_bch_usd_price, sender=Block)
