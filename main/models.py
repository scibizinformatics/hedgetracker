from django.db import models


class Block(models.Model):
    height = models.IntegerField() 
    timestamp = models.DateTimeField()

class Funding(models.Model):
    address = models.CharField(max_length=60)
    transaction = models.CharField(max_length=70)
    output_index = models.IntegerField()
    low_liquidation_price = models.IntegerField()
    high_liquidation_price = models.IntegerField()
    earliest_liquidation_height = models.IntegerField()
    maturity_height = models.IntegerField()
    maturity_block = models.ForeignKey(
        Block,
        related_name='funding_transactions',
        on_delete=models.CASCADE
    )
    low_truncated_zeroes = models.CharField(max_length=10)
    high_low_delta_truncated_zeroes = models.CharField(max_length=10)
    hedge_units_x_sats_per_bch_high_trunc = models.IntegerField()
    payout_sats_low_trunc = models.IntegerField()

class Settlement(models.Model):
    funding = models.OneToOneField(
        Funding,
        on_delete=models.CASCADE
    )
    spending_transaction = models.CharField(max_length=70)
    settlement_type = models.CharField(max_length=20)
    hedge_satoshis = models.IntegerField()
    long_satoshis = models.IntegerField()
    oracle_price = models.IntegerField()
