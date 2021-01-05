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
        transaction=data['funding']['fundingTransaction']
    )
    funding.save()
    settlement = Settlement(
        funding=funding,
        settlement_type=data['settlement']['settlementType']
    )
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
        req.include_mempool = True
        req.serialize_tx = True
        req.subscribe.CopyFrom(tx_filter)

        for notification in stub.SubscribeTransactions(req):
            raw_tx_hex = notification.serialized_transaction.hex()
            parsed_tx = contract_parser.detect_and_parse(raw_tx_hex)
            logger.info(parsed_tx)
            if parsed_tx:
                save_settlement(parsed_tx)
                logger.info('Saved tx!')
