from django.urls import re_path, path

from apps.chats import consumers


websocket_urlpatterns = [
    path(r'chat', consumers.ChatsConsumer.as_asgi()),
]
