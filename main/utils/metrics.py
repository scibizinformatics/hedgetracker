from main.models import (
    Settlement,
    Metric,
)


class MetricsHandler(object):

    def __init__(self, settlement_id):
        self.SETTLEMENT = Settlement.objects.get(id=settlement_id)
        self.APPROX_FUNDING_PRICE = self.SETTLEMENT.funding.transaction_block.bch_usd_price
        self.APPROX_FUNDING_PRICE *= 100
        self.SATOSHI_DECIMAL = 100000000
        self.HEDGE = 'hedge'
        self.LONG = 'long'

    
    def compute_metrics(self):
        total_contract_satoshis = self.get_total_contract_satoshis()
        hedge_usd_payout = self.get_usd_payout(self.HEDGE)
        long_usd_payout = self.get_usd_payout(self.LONG)

        approx_hedge_payin_satoshis = self.get_approx_hedge_payin_satoshis(hedge_usd_payout)
        approx_long_payin_satoshis = total_contract_satoshis - approx_hedge_payin_satoshis

        approx_hedge_usd_payin = self.get_approx_usd_payin(approx_hedge_payin_satoshis)
        approx_long_usd_payin = self.get_approx_usd_payin(approx_long_payin_satoshis)

        approx_hedge_gain = hedge_usd_payout - approx_hedge_usd_payin
        approx_long_gain = long_usd_payout - approx_long_usd_payin


        metric = Metric(
            total_contract_satoshis=total_contract_satoshis,
            hedge_usd_payout=hedge_usd_payout,
            long_usd_payout=long_usd_payout,

            approx_hedge_payin_satoshis=approx_hedge_payin_satoshis,
            approx_long_payin_satoshis=approx_long_payin_satoshis,
            
            approx_hedge_usd_payin=approx_hedge_usd_payin,
            approx_long_usd_payin=approx_long_usd_payin,

            approx_hedge_gain=approx_hedge_gain,
            approx_long_gain=approx_long_gain
        )
        metric.save()

    
    def get_total_contract_satoshis(self):
        return self.SETTLEMENT.hedge_satoshis + self.SETTLEMENT.long_satoshis


    def get_usd_payout(self, position_type):
        settlement_satoshis = 0

        if position_type == self.HEDGE:
            settlement_satoshis = self.SETTLEMENT.hedge_satoshis
        elif position_type == self.LONG:
            settlement_satoshis = self.SETTLEMENT.long_satoshis

        satoshis = settlement_satoshis / self.SATOSHI_DECIMAL
        return satoshis * self.SETTLEMENT.oracle_price


    def get_approx_hedge_payin_satoshis(self, hedge_usd_payout):
        price_during_funding_txn = hedge_usd_payout / self.APPROX_FUNDING_PRICE
        return price_during_funding_txn * self.SATOSHI_DECIMAL


    def get_approx_usd_payin(self, approx_payin_satoshis):
        converted_approx_payin_sats = approx_payin_satoshis / self.SATOSHI_DECIMAL
        return converted_approx_payin_sats * self.APPROX_FUNDING_PRICE
        
