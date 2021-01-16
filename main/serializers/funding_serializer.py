from rest_framework import serializers


from main.serializers.block_serializer import BlockSerializer
from main.models import Funding


class FundingSerializer(serializers.ModelSerializer):
    transaction_block = BlockSerializer()
    maturity_block = BlockSerializer()
    
    class Meta:
        model = Funding
        fields = (
            'address',
            'transaction',
            'transaction_block',
            'output_index',
            'low_liquidation_price',
            'high_liquidation_price',
            'earliest_liquidation_height',
            'maturity_height',
            'maturity_block',
            'low_truncated_zeroes',
            'high_low_delta_truncated_zeroes',
            'hedge_units_x_sats_per_bch_high_trunc',
            'payout_sats_low_trunc',
        )
