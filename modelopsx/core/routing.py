from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/shell/live/$', consumers.InteractiveSSHConsumer.as_asgi()),
]
