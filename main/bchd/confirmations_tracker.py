from datetime import datetime
import grpc
import time
import logging
import requests
import pytz

import sys
sys.path.append('/app/main/bchd/protobuf')

import bchrpc_pb2 as pb
import bchrpc_pb2_grpc as bchrpc

from main.models import Settlement, Block

logger = logging.getLogger(__name__)


def save_confirmation(txid, block_height):
    settlement = Settlement.objects.filter(spending_transaction=txid)
    block_check = Block.objects.filter(height=block_height)
    if block_check.exists():
        settlement.block = block_check.first()
        settlement.save()
    else:
        url = 'https://bchd.fountainhead.cash/v1/GetBlockInfo'
        resp = requests.post(url, json={'height': block_height})
        timestamp = int(resp.json()['info']['timestamp'])
        block = Block(
            height=block_height,
            timestamp=datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        )
        block.save()
        settlement.block = block
        settlement.save()


def run():
    logger.info('Running the tracker...')
    creds = grpc.ssl_channel_credentials()
    with grpc.secure_channel('bchd.ny1.simpleledger.io', creds) as channel:
        stub = bchrpc.bchrpcStub(channel)

        req = pb.GetBlockchainInfoRequest()
        resp = stub.GetBlockchainInfo(req)

        tx_filter = pb.TransactionFilter()
        tx_filter.all_transactions = True

        req = pb.SubscribeTransactionsRequest()
        req.include_in_block = True
        req.subscribe.CopyFrom(tx_filter)

        for notification in stub.SubscribeTransactions(req):
            tx = notification.unconfirmed_transaction.transaction
            tx_hash = bytearray(tx.hash[::-1]).hex()
            save_confirmation(tx_hash, tx.block_height)
            logger.info('Saved confirmation!')
