from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings


# send real time data
def send_rt_data(data_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.MAIN_ROOM,
        {
            "type": "send_update",
            "operation": data_type, 
            "data": data
        }
    )
