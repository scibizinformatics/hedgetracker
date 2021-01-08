import grpc
import time
import logging

import sys
sys.path.append('/app/main/bchd/protobuf')

import bchrpc_pb2 as pb
import bchrpc_pb2_grpc as bchrpc

from main.anyhedge import contract_parser
from main.models import Funding, Settlement

logger = logging.getLogger(__name__)


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
        req.include_mempool = True
        req.serialize_tx = True
        req.subscribe.CopyFrom(tx_filter)

        for notification in stub.SubscribeTransactions(req):
            raw_tx_hex = notification.serialized_transaction.hex()
            parsed_tx = contract_parser.detect_and_parse(raw_tx_hex)
            if parsed_tx:
                save_settlement(parsed_tx)
