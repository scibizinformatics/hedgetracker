from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
# from main.serializers import AlertSerializer


def send_Alert(message, notif_type, data={}):

    # Alert = create_Alert(user, message, notif_type, data)
    # Alert = AlertSerializer(Alert)
    data = {'name': 'reamon'}

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{settings.MAIN_ROOM}_{settings.MAIN_CHANNEL}", 
        {
            "type": "send_update",
            "operation": "alert", 
            "data": data
        }
    )
