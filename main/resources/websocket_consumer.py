from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.conf import settings
import json
import logging


logger = logging.getLogger(__name__)


class MainConsumer(WebsocketConsumer):
    """
        This websocket is for sending real-time datapoints.
    """

    def connect(self):
        self.room_name = f"{settings.MAIN_ROOM}"
        self.channel_name = f"{settings.MAIN_CHANNEL}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        self.accept()
        logger.info("Websocket connected!")


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        logger.info("Websocket disonnected.")


    def send_update(self, data):
        data['type'] = data['operation']
        del data['operation']
        self.send(text_data=json.dumps(data))
