from django.db.models import (
    Sum,
    Avg,
    F,
)

from main.models import (
    Settlement,
    Metric,
)

from django.conf import settings


class MetricsHandler(object):

    def __init__(self, settlement_qs, date_created=None):
        self.settlement_qs = settlement_qs
        self.date_created = date_created
        # self.APPROX_FUNDING_PRICE *= 100
        self.HEDGE = 'hedge'
        self.LONG = 'long'
        
        self.TOTAL = 'total'
        self.AVG = 'avg'

    
    def compute_metrics(self):
        total_contract_satoshis = self.get_total_contract_satoshis()

        usd_payouts = {'total': {}, 'avg': {}}
        usd_payouts['total']['hedge'], usd_payouts['total']['long'] = self.get_usd_payouts(self.TOTAL)
        usd_payouts['avg']['hedge'], usd_payouts['avg']['long'] = self.get_usd_payouts(self.AVG)

        # approx_hedge_payin_satoshis = self.get_approx_hedge_payin_satoshis(hedge_usd_payout)
        # approx_long_payin_satoshis = total_contract_satoshis - approx_hedge_payin_satoshis

        # approx_hedge_usd_payin = self.get_approx_usd_payin(approx_hedge_payin_satoshis)
        # approx_long_usd_payin = self.get_approx_usd_payin(approx_long_payin_satoshis)

        # approx_hedge_gain = hedge_usd_payout - approx_hedge_usd_payin
        # approx_long_gain = long_usd_payout - approx_long_usd_payin


        metric = Metric(
            total_contract_satoshis=total_contract_satoshis,
            usd_payouts=usd_payouts

            # approx_hedge_payin_satoshis=approx_hedge_payin_satoshis,
            # approx_long_payin_satoshis=approx_long_payin_satoshis,
            
            # approx_hedge_usd_payin=approx_hedge_usd_payin,
            # approx_long_usd_payin=approx_long_usd_payin,

            # approx_hedge_gain=approx_hedge_gain,
            # approx_long_gain=approx_long_gain
        )
        metric.save()

        if self.date_created:
            Metric.objects.filter(id=metric.id).update(
                date_created=self.date_created
            )

    
    def get_total_contract_satoshis(self):
        total = self.settlement_qs.aggregate(
            total=Sum(F('hedge_satoshis') + F('long_satoshis'))
        )['total']
        
        if total is None:
            total = 0
        return total


    def get_usd_payouts(self, aggregate_type):
        hedge_exp = (F('hedge_satoshis') / settings.SATOSHI_DECIMAL) * F('oracle_price')
        long_exp = (F('long_satoshis') / settings.SATOSHI_DECIMAL) * F('oracle_price')
        
        if aggregate_type == self.TOTAL:
            hedge_exp = Sum(hedge_exp)
            long_exp = Sum(long_exp)
        elif aggregate_type == self.AVG:
            hedge_exp = Avg(hedge_exp)
            long_exp = Avg(long_exp)
        
        payouts = self.settlement_qs.aggregate(hedge=hedge_exp, long=long_exp)

        try:
            hp = payouts['hedge'] / 100
            lp = payouts['long'] / 100
        except TypeError:
            hp = 0
            lp = 0
        
        return hp, lp


    # def get_approx_hedge_payin_satoshis(self, hedge_usd_payout):
    #     price_during_funding_txn = hedge_usd_payout / self.APPROX_FUNDING_PRICE
    #     return price_during_funding_txn * self.SATOSHI_DECIMAL


    # def get_approx_usd_payin(self, approx_payin_satoshis):
    #     converted_approx_payin_sats = approx_payin_satoshis / self.SATOSHI_DECIMAL
    #     return converted_approx_payin_sats * self.APPROX_FUNDING_PRICE
