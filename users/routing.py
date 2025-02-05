from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/manager-chat/(?P<chat_id>\d+)/(?P<user_id>\d+)$", consumers.CreateEmployeeMessage.as_asgi()),
]
