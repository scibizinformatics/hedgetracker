from django.db.models.signals import post_save
from main.models import Funding, Block
from datetime import datetime
import requests
import pytz


def associate_block(sender, instance, **kwargs):
    block_check = Block.objects.filter(height=instance.maturity_height)
    if block_check.exists():
        instance.update(maturity_block=block_check.first())
    else:
        url = 'https://bchd.fountainhead.cash/v1/GetBlockInfo'
        resp = requests.post(url, json={'height': instance.maturity_height})
        timestamp = int(resp.json()['info']['timestamp'])
        block = Block(
            height=instance.maturity_height,
            timestamp=datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        )
        block.save()
        instance.update(maturity_block=block)

# Catch changes in Funding & Settlement


post_save.connect(associate_block, sender=Funding)
