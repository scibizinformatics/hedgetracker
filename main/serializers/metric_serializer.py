from rest_framework import serializers

from main.models import Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class MetricListSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    total_contract_satoshis = serializers.SerializerMethodField()
    hedge_usd_payout = serializers.SerializerMethodField()
    long_usd_payout = serializers.SerializerMethodField()
    # approx_hedge_payin_satoshis = serializers.SerializerMethodField()
    # approx_long_payin_satoshis = serializers.SerializerMethodField()
    approx_long_usd_payin = serializers.SerializerMethodField()
    approx_hedge_usd_payin = serializers.SerializerMethodField()

    approx_hedge_gain = serializers.SerializerMethodField()
    approx_long_gain = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = Metric
        fields = (
            # 'id',
            'total_contract_satoshis',
            'hedge_usd_payout',
            'long_usd_payout',
            # 'approx_hedge_payin_satoshis',
            # 'approx_long_payin_satoshis',
            'approx_hedge_usd_payin',
            'approx_long_usd_payin',

            'approx_hedge_gain',
            'approx_long_gain',
            'date_created',
        )

    # def get_id(self, metric):
    #     return Metric.objects.values_list('id', flat=True)

    def get_total_contract_satoshis(self, metric):
        return Metric.objects.values_list('total_contract_satoshis', flat=True)

    def get_hedge_usd_payout(self, metric):
        return Metric.objects.values_list('hedge_usd_payout', flat=True)

    def get_long_usd_payout(self, metric):
        return Metric.objects.values_list('long_usd_payout', flat=True)

    # def get_approx_hedge_payin_satoshis(self, metric):
    #     return Metric.objects.values_list('approx_hedge_payin_satoshis', flat=True)

    # def get_approx_long_payin_satoshis(self, metric):
    #     return Metric.objects.values_list('approx_long_payin_satoshis', flat=True)

    def get_approx_hedge_usd_payin(self, metric):
        return Metric.objects.values_list('approx_hedge_usd_payin', flat=True)

    def get_approx_long_usd_payin(self, metric):
        return Metric.objects.values_list('approx_long_usd_payin', flat=True)

    def get_approx_hedge_gain(self, metric):
        return Metric.objects.values_list('approx_hedge_gain', flat=True)
        
    def get_approx_long_gain(self, metric):
        return Metric.objects.values_list('approx_long_gain', flat=True)
        
    def get_date_created(self, metric):
        return Metric.objects.values_list('date_created', flat=True)
