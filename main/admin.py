from django.contrib import admin

from main.models import *


admin.site.site_header = 'Hedge Tracker Admin'


class BlockAdmin(admin.ModelAdmin):
    list_display = [
        'height',
        'timestamp',
        'bch_usd_price',
    ]


class FundingAdmin(admin.ModelAdmin):
    list_display = [
        'address',
        'transaction',
        'output_index',
        'maturity_height',
        'maturity_block',
    ]


class SettlementAdmin(admin.ModelAdmin):
    list_display = [
        'funding',
        'spending_transaction',
        'settlement_type',
        'hedge_satoshis',
        'long_satoshis',
        'oracle_price',
        'block',
    ]


class MetricAdmin(admin.ModelAdmin):
    list_display = [
        'date_created',
    ]


admin.site.register(Block, BlockAdmin)
admin.site.register(Funding, FundingAdmin)
admin.site.register(Settlement, SettlementAdmin)
admin.site.register(Metric, MetricAdmin)
