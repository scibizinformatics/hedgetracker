from django.contrib import admin

from main.models import *


admin.site.site_header = 'Hedge Tracker Admin'


class BlockAdmin(admin.ModelAdmin):
    list_display = [
        'height',
        'timestamp',
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


admin.site.register(Block, BlockAdmin)
admin.site.register(Funding, FundingAdmin)
admin.site.register(Settlement, SettlementAdmin)
