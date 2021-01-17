import os
import time
import base64
import logging
import requests
import collections

import sys
sys.path.append('/app/main/bchd/protobuf')

import bchrpc_pb2 as pb

from django.conf import settings
from main.anyhedge import contract_parser
from main.models import Funding, Settlement, Block
from main.helpers import ts_to_date, get_block_info

logger = logging.getLogger(__name__)


def get_raw_transaction_hex(txhash):
    req = pb.GetRawTransactionRequest()
    req.hash = bytes.fromhex(txhash)[::-1]
    resp = settings.GRPC_STUB.GetRawTransaction(req)
    return resp.transaction.hex()


def get_funding_txn_block(txhash):
    req = pb.GetTransactionRequest()
    req.hash = bytes.fromhex(txhash)[::-1]
    resp = settings.GRPC_STUB.GetTransaction(req)

    funding_txn_block, created = Block.objects.get_or_create(
        height=resp.transaction.block_height,
        timestamp=ts_to_date(resp.transaction.timestamp)
    )

    return funding_txn_block


def save_settlement(data):
    txhash = data['funding']['fundingTransaction']
    funding_txn_block = get_funding_txn_block(txhash)

    funding = Funding(
        address=data['address'],
        transaction=txhash,
        transaction_block=funding_txn_block,
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
            height, timestamp = get_block_info(height=block_height)
            block = Block(
                height=block_height,
                timestamp=ts_to_date(timestamp)
            )
            block.save()
            settlement.block = block
            settlement.save()
        logger.info('Confirmed Tx @ {0}: {1}'.format(block_height, txid))


def run():
    logger.info('Running the transactions tracker...')

    req = pb.GetBlockchainInfoRequest()
    resp = settings.GRPC_STUB.GetBlockchainInfo(req)
    logger.info(resp)

    tx_filter = pb.TransactionFilter()
    tx_filter.all_transactions = True

    req = pb.SubscribeTransactionsRequest()
    req.include_in_block = True
    req.include_mempool = True
    req.include_in_block = True
    req.subscribe.CopyFrom(tx_filter)

    parsed_txs = collections.deque(maxlen=10000)

    for notification in settings.GRPC_STUB.SubscribeTransactions(req):
        tx = notification.unconfirmed_transaction.transaction
        confirmed = False
        if len(tx.hash) > 0:
            tx = notification.unconfirmed_transaction.transaction
        else:
            confirmed = True
            tx = notification.confirmed_transaction

        tx_hash = bytearray(tx.hash[::-1]).hex()
        log_msg = 'tx: {0} | confirmed: {1} [{2}]'.format(tx_hash, str(confirmed).lower(), tx.block_height)

        if len(tx.inputs) == 1 and len(tx.outputs) == 2:
            if tx.outputs[0].script_class == 'pubkeyhash' and tx.outputs[1].script_class == 'pubkeyhash':
                if hash(tx_hash) not in parsed_txs:
                    log_msg += ' *'
                    if not Settlement.objects.filter(spending_transaction=tx_hash).exists():
                        height, timestamp = get_block_info(height=tx.block_height)
                        block, created = Block.objects.get_or_create(
                            height=height,
                            timestamp=ts_to_date(timestamp)
                        )

                        raw_tx_hex = get_raw_transaction_hex(tx_hash)
                        parsed_tx = contract_parser.detect_and_parse(raw_tx_hex)
                        if parsed_tx:
                            save_settlement(parsed_tx)
                    parsed_txs.append(hash(tx_hash))
        logger.info(log_msg)

        if confirmed:
            process_confirmation(tx_hash, tx.block_height)
