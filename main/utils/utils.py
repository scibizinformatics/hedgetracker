from datetime import datetime
import requests
import logging
import pytz
import sys

sys.path.append('/app/main/bchd/protobuf')

import bchrpc_pb2 as pb
from django.conf import settings

logger = logging.getLogger(__name__)


def ts_to_date(timestamp):
    return datetime.fromtimestamp(
        timestamp
    ).replace(tzinfo=pytz.utc)


def get_BCH_USD_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin-cash&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()

    return data['bitcoin-cash']['usd']


def get_block_info(txhash=None, height=None):
    req = pb.GetBlockInfoRequest()
    if txhash:
        req.hash = txhash
    if height:
        req.height = height

    resp = settings.GRPC_STUB.GetBlockInfo(req)
    return resp.info.height, resp.info.timestamp
