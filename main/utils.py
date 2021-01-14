from datetime import datetime
import requests
import pytz


def ts_to_date(timestamp):
    return datetime.fromtimestamp(
        timestamp
    ).replace(tzinfo=pytz.utc)


def get_BCH_USD_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin-cash&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()

    return data['bitcoin-cash']['usd']
