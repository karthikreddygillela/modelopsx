import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import core.routing  # or whatever your app is named

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modelopsx.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns  # must point to your app's routing.py
        )
    ),
})
