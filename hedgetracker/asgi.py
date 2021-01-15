import os
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hedgetracker.settings')
from main.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(
      URLRouter(websocket_urlpatterns),
      ["*"] # Change this to dedicated domain to restrict multiple incoming connections
    )
})