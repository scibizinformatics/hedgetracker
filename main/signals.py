from django.db.models.signals import post_save

from main.utils import ts_to_date, get_BCH_USD_price
from main.models import Funding, Block

import requests


def associate_block(sender, instance, **kwargs):
    block_check = Block.objects.filter(height=instance.maturity_height)
    if block_check.exists():
        instance.maturity_block = block_check.first()
    else:
        url = 'https://bchd.fountainhead.cash/v1/GetBlockInfo'
        resp = requests.post(url, json={'height': instance.maturity_height})
        timestamp = int(resp.json()['info']['timestamp'])
        block, created = Block.objects.get_or_create(
            height=instance.maturity_height,
            timestamp=ts_to_date(timestamp)
        )
        instance.maturity_block = block
    instance.save()


def save_bch_usd_price(sender, instance, **kwargs):
    price = get_BCH_USD_price()
    instance.bch_usd_price = price
    instance.save()


post_save.connect(associate_block, sender=Funding)
post_save.connect(save_bch_usd_price, sender=Block)
