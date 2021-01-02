#!/usr/bin/env python3
import grpc
import bchrpc_pb2 as pb
import bchrpc_pb2_grpc as bchrpc
import time

def run():
    creds = grpc.ssl_channel_credentials(open('bchd.spice.cash.crt', 'rb').read())
    with grpc.secure_channel('bchd.spice.cash:8335', creds) as channel:
    #creds = grpc.ssl_channel_credentials()
    #with grpc.secure_channel('bchd.ny1.simpleledger.io', creds) as channel:
        stub = bchrpc.bchrpcStub(channel)

        req = pb.GetBlockchainInfoRequest()
        resp = stub.GetBlockchainInfo(req)
        print(resp)

        tx_filter = pb.TransactionFilter()
        tx_filter.all_transactions = True

        req = pb.SubscribeTransactionsRequest()
        req.include_in_block = True
        req.include_mempool = True
        req.include_in_block = True
        req.subscribe.CopyFrom(tx_filter)

        for notification in stub.SubscribeTransactions(req):
            print('\n################# BEGIN ######################\n')
            tx = notification.unconfirmed_transaction.transaction
            if len(tx.hash) > 0:
                print('confirmed: false')
                tx = notification.unconfirmed_transaction.transaction
            else:
                tx = notification.confirmed_transaction
                print('confirmed: true')
                print('blockheight: ' + str(tx.block_height))
            tx_hash = bytearray(tx.hash[::-1]).hex()
            print('hash: ' + tx_hash)
            print('\n-----------------------------------------------\n')
            print('INPUTS\n\n')
            for tx_input in tx.inputs:
                print('index: ' + str(tx_input.index))
                print('value: ' + str(tx_input.value))
                print('address: bitcoincash:' + tx_input.address)
                print('outpoint:')
                outpoint_hash = bytearray(tx_input.outpoint.hash[::-1]).hex()
                print('  hash: ' + outpoint_hash)
                print('  index: ' + str(tx_input.outpoint.index))
                print('\n')
            print('-----------------------------------------------\n')
            print('OUTPUTS\n\n')
            has_op_return_data = False
            for output in tx.outputs:
                print('index: ' + str(output.index))
                print('value: ' + str(output.value))
                print('address: bitcoincash:' + output.address)
                print('script_class: ' + output.script_class)
                if output.script_class == 'datacarrier':
                    has_op_return_data = True
                if has_op_return_data:
                    if output.slp_token.token_id:
                        token_id = bytearray(output.slp_token.token_id).hex()
                        print('token_id: ' + token_id)
                        print('slp_address: simpleledger:' + output.slp_token.address)
                        formatted_amount = output.slp_token.amount / (10 ** output.slp_token.decimals)
                        print('amount: ' + str(formatted_amount))
                print('\n')
            print('-----------------------------------------------')
            print('\n################## END ########################\n')

        # # Get block and parse tx hashes contained in block
        # req = pb.GetBlockRequest()
        # req.height = 271012
        # req.full_transactions = True

        # resp = stub.GetBlock(req)

        # hash = resp.block.info.hash
        # hash = bytearray(hash[::-1])

        # for tx in resp.block.transaction_data:
        #     txhash = bytearray(tx.transaction.hash[::-1])
        #     print(txhash.hex())

if __name__ == '__main__':
    run()
