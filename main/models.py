from django.utils import timezone
from django.db import models


class Block(models.Model):
    height = models.IntegerField() 
    timestamp = models.DateTimeField()
    bch_usd_price = models.FloatField(default=0)

    class Meta:
        ordering = ('-timestamp', )


class Funding(models.Model):
    address = models.CharField(max_length=60)
    transaction = models.CharField(max_length=70)
    transaction_block = models.ForeignKey(
        Block,
        related_name='funding_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    output_index = models.IntegerField()
    low_liquidation_price = models.FloatField()
    high_liquidation_price = models.FloatField()
    earliest_liquidation_height = models.IntegerField()
    maturity_height = models.IntegerField()
    maturity_block = models.ForeignKey(
        Block,
        related_name='matured_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    low_truncated_zeroes = models.CharField(max_length=10)
    high_low_delta_truncated_zeroes = models.CharField(max_length=10)
    hedge_units_x_sats_per_bch_high_trunc = models.FloatField()
    payout_sats_low_trunc = models.FloatField()

    class Meta:
        ordering = ('-transaction_block__timestamp', )


class Settlement(models.Model):
    funding = models.OneToOneField(
        Funding,
        on_delete=models.CASCADE
    )
    spending_transaction = models.CharField(max_length=70)
    settlement_type = models.CharField(max_length=20)
    hedge_satoshis = models.FloatField()
    long_satoshis = models.FloatField()
    oracle_price = models.FloatField()
    block = models.ForeignKey(
        Block,
        related_name='settlement_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-block__timestamp', )


class Metric(models.Model):
    total_contract_satoshis = models.FloatField()
    hedge_usd_payout = models.FloatField()
    long_usd_payout = models.FloatField()
    approx_hedge_payin_satoshis = models.FloatField()
    approx_long_payin_satoshis = models.FloatField()
    approx_hedge_usd_payin = models.FloatField(default=0)
    approx_long_usd_payin = models.FloatField()

    approx_hedge_gain = models.FloatField(default=0)
    approx_long_gain = models.FloatField(default=0)

    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('date_created', )
