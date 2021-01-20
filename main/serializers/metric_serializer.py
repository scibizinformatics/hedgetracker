from rest_framework import serializers

from main.models import Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class MetricListSerializer(serializers.ModelSerializer):
    total_contract_satoshis = serializers.SerializerMethodField()
    usd_payouts = serializers.SerializerMethodField()
    # approx_hedge_payin_satoshis = serializers.SerializerMethodField()
    # approx_long_payin_satoshis = serializers.SerializerMethodField()
    # approx_long_usd_payin = serializers.SerializerMethodField()
    # approx_hedge_usd_payin = serializers.SerializerMethodField()

    # approx_hedge_gain = serializers.SerializerMethodField()
    # approx_long_gain = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = Metric
        fields = (
            'total_contract_satoshis',
            'usd_payouts',
            # 'approx_hedge_payin_satoshis',
            # 'approx_long_payin_satoshis',
            # 'approx_hedge_usd_payin',
            # 'approx_long_usd_payin',

            # 'approx_hedge_gain',
            # 'approx_long_gain',
            'date_created',
        )


    def get_total_contract_satoshis(self, metric):
        return Metric.objects.values_list('total_contract_satoshis', flat=True)

    def get_usd_payouts(self, metric):
        usd_payouts = {'total': {}, 'avg': {}}
        usd_payouts['total']['hedge'] = Metric.objects.values_list('usd_payouts__total__hedge', flat=True)
        usd_payouts['total']['long'] = Metric.objects.values_list('usd_payouts__total__long', flat=True)
        usd_payouts['avg']['hedge'] = Metric.objects.values_list('usd_payouts__avg__hedge', flat=True)
        usd_payouts['avg']['long'] = Metric.objects.values_list('usd_payouts__avg__long', flat=True)
        return usd_payouts

    # def get_approx_hedge_payin_satoshis(self, metric):
    #     return Metric.objects.values_list('approx_hedge_payin_satoshis', flat=True)

    # def get_approx_long_payin_satoshis(self, metric):
    #     return Metric.objects.values_list('approx_long_payin_satoshis', flat=True)

    # def get_approx_hedge_usd_payin(self, metric):
    #     return Metric.objects.values_list('approx_hedge_usd_payin', flat=True)

    # def get_approx_long_usd_payin(self, metric):
    #     return Metric.objects.values_list('approx_long_usd_payin', flat=True)

    # def get_approx_hedge_gain(self, metric):
    #     return Metric.objects.values_list('approx_hedge_gain', flat=True)
        
    # def get_approx_long_gain(self, metric):
    #     return Metric.objects.values_list('approx_long_gain', flat=True)
        
    def get_date_created(self, metric):
        return Metric.objects.values_list('date_created', flat=True)
