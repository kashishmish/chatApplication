# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<user_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/personalchat/(?P<me>\w+)/(?P<you>\w+)/$', consumers.PersonalConsumer.as_asgi()),
    re_path(r'ws/loginstatus/(?P<username>\w+)/$', consumers.LoginStatus.as_asgi()),
]