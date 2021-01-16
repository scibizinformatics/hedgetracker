from rest_framework import serializers

from main.serializers.funding_serializer import FundingSerializer
from main.serializers.block_serializer import BlockSerializer
from main.models import Settlement


class SettlementSerializer(serializers.ModelSerializer):
    funding = FundingSerializer()
    block = BlockSerializer()
    
    class Meta:
        model = Settlement
        fields = (
            'funding',
            'spending_transaction',
            'settlement_type',
            'hedge_satoshis',
            'long_satoshis',
            'oracle_price',
            'block',
        )
