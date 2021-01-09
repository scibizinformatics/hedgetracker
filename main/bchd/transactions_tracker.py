import grpc
import time
import pytz
import base64
import logging
import requests
from datetime import datetime

import sys
sys.path.append('/app/main/bchd/protobuf')

import bchrpc_pb2 as pb
import bchrpc_pb2_grpc as bchrpc

from main.anyhedge import contract_parser
from main.models import Funding, Settlement, Block

logger = logging.getLogger(__name__)


def get_raw_transaction_hex(txhash):
    rev_bytes_arr = bytearray.fromhex(txhash)[::-1]
    bchd_txhash = base64.b64encode(rev_bytes_arr).decode()
    url = 'https://bchd.fountainhead.cash/v1/GetRawTransaction'
    resp = requests(url, json={ 'hash': bchd_txhash })
    raw_tx_b64 = resp.json()['transaction']
    return base64.b64decode(raw_tx_b64).hex()


def save_settlement(data):
    funding = Funding(
        address=data['address'],
        transaction=data['funding']['fundingTransaction'],
        output_index=data['funding']['fundingOutput'],
        low_liquidation_price=data['parameters']['lowLiquidationPrice'],
        high_liquidation_price=data['parameters']['highLiquidationPrice'],
        earliest_liquidation_height=data['parameters']['earliestLiquidationHeight'],
        maturity_height=data['parameters']['maturityHeight'],
        low_truncated_zeroes=data['parameters']['lowTruncatedZeroes'],
        high_low_delta_truncated_zeroes=data['parameters']['highLowDeltaTruncatedZeroes'],
        hedge_units_x_sats_per_bch_high_trunc=data['parameters']['hedgeUnitsXSatsPerBchHighTrunc'],
        payout_sats_low_trunc=data['parameters']['payoutSatsLowTrunc']
    )
    funding.save()
    settlement = Settlement(
        funding=funding,
        spending_transaction=data['settlement']['spendingTransaction'],
        settlement_type=data['settlement']['settlementType'],
        hedge_satoshis=data['settlement']['hedgeSatoshis'],
        long_satoshis=data['settlement']['longSatoshis'],
        oracle_price=data['settlement']['oraclePrice']
    )
    settlement.save()
    logger.info('Settlement transaction: {0}'.format(settlement.spending_transaction))


def process_confirmation(txid, block_height):
    settlement_check = Settlement.objects.filter(spending_transaction=txid)
    if settlement_check.exists():
        settlement = settlement_check.first()
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
        logger.info('Confirmed Tx @ {0}: {1}'.format(block_height, txid))


def run():
    logger.info('Running the transactions tracker...')
    creds = grpc.ssl_channel_credentials()
    with grpc.secure_channel('bchd.ny1.simpleledger.io', creds) as channel:
        stub = bchrpc.bchrpcStub(channel)

        req = pb.GetBlockchainInfoRequest()
        resp = stub.GetBlockchainInfo(req)
        logger.info(resp)

        tx_filter = pb.TransactionFilter()
        tx_filter.all_transactions = True

        req = pb.SubscribeTransactionsRequest()
        req.include_in_block = True
        req.include_mempool = True
        req.include_in_block = True
        req.subscribe.CopyFrom(tx_filter)

        for notification in stub.SubscribeTransactions(req):
            tx = notification.unconfirmed_transaction.transaction
            confirmed = False
            if len(tx.hash) > 0:
                tx = notification.unconfirmed_transaction.transaction
            else:
                confirmed = True
                tx = notification.confirmed_transaction

            tx_hash = bytearray(tx.hash[::-1]).hex()
            if confirmed:
                process_confirmation(tx_hash, tx.block_height)

            if len(tx.inputs) == 1 and len(tx.outputs) == 2:
                raw_tx_hex = get_raw_transaction_hex(tx_hash)
                parsed_tx = contract_parser.detect_and_parse(raw_tx_hex)
                if parsed_tx:
                    save_settlement(parsed_tx)
